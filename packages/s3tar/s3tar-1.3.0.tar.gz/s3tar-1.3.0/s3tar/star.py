"""s3tar main module.

entry point: star()
"""
import datetime
import glob
import os
import random
import re
import shutil
import sys
import tarfile
import tempfile
import time

import click

from s3tar import __version__
from ccaaws.s3filesystem import S3FileSystem
from ccautils.errors import errorExit


@click.group()
def cli():
    pass


tre = re.compile(".*[._-]{1}([0-9-]{10}T[0-9:]{8}).*")


def displayTS(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.isoformat()


def makeTsFromLength(length, startts):
    try:
        ll = length[-1:]
        xl = int(length[:-1])
        mult = 0
        ets = startts
        if ll == "h":
            mult = 3600
        elif ll == "d":
            mult = 86400
        elif ll == "w":
            mult = 86400 * 7
        zl = xl * mult
        if zl > 0:
            ets = startts + zl
        return ets
    except Exception as e:
        msg = f"failed to decode '{length}' into a sane length of time"
        msg += f"\nException: {e}"
        errorExit("makeTsFromStr", msg)


def makeTsFromStr(dtstr):
    try:
        if dtstr.isnumeric() and len(dtstr) == 10:
            ts = int(dtstr)
        else:
            dt = datetime.datetime.fromisoformat(dtstr)
            ts = dt.timestamp()
        return ts
    except Exception as e:
        msg = f"failed to decode '{dtstr}' into a date/time"
        errorExit("makeTsFromStr", msg)


def buildUriFromPath(path):
    if path.startswith("/"):
        uri = f"s3:/{path}"
    elif not path.startswith("s3://") and not path.startswith("https://"):
        uri = f"s3://{path}"
    else:
        uri = path
    if not uri.endswith("/"):
        uri += "/"
    return uri


def filterByName(objects, name):
    try:
        objs = [obj for obj in objects if name in obj["Key"]]
        return objs
    except Exception as e:
        msg = f"failed to filter by name: {name}"
        msg += f"\nException {e}"
        errorExit("filterByName", msg)


def filterRE(name, sts, ets):
    ts = ets
    try:
        m = tre.match(name)
        if m is not None:
            dt = datetime.datetime.fromisoformat(m[1])
            ts = dt.timestamp()
            if ts >= sts and ts <= ets:
                return (ts, True)
        return (ts, False)
    except Exception as e:
        msg = f"failed to filterRE name {name}, sts {sts}, ets {ets}"
        msg += f"\nException {e}"
        errorExit("filterRE", msg)


def filterTS(obj, sts, ets):
    try:
        dt = obj["LastModified"]
        ts = dt.timestamp()
        if ts >= sts and ts <= ets:
            return (ts, True)
        return (ts, False)
    except Exception as e:
        msg = f"failed to filterTS object {obj}, sts {sts}, ets {ets}"
        msg += f"\nException {e}"
        errorExit("filterTS", msg)


def filterObjs(objects, sts, ets, name=None, uselmts=False):
    try:
        op = {}
        xobjs = filterByName(objects, name) if name is not None else objects
        for obj in xobjs:
            if uselmts:
                ts, state = filterTS(obj, sts, ets)
                if state:
                    op[ts] = obj
            elif sts == 0:
                dt = obj["LastModified"]
                ts = dt.timestamp()
                op[ts] = obj
            else:
                ts, state = filterRE(obj["Key"], sts, ets)
                if state:
                    op[ts] = obj
        return op
    except Exception as e:
        msg = f"failed to filter xobjs: sts {sts}, ets {ets}, name {name}, uselmts {uselmts}"
        msg += f"\nException: {e}"
        errorExit("filterObjs", msg)


@cli.command()
@click.option(
    "-c",
    "--compression",
    type=click.STRING,
    help="optional compression ['b', 'g', 'n', 'z'], default 'g'",
)
@click.option("-e", "--end", type=click.STRING, help="optional end time")
@click.option(
    "-l", "--length", type=click.STRING, help="optional time length (i.e. 1d, 3h, 4w)"
)
@click.option(
    "-M",
    "--usemodified",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="use last modified time stamp rather than filename for filtering",
)
@click.option("-N", "--name", type=click.STRING, help="optional name filter")
@click.option(
    "-o", "--output", type=click.STRING, help="output file name (default: bucket name)"
)
@click.option(
    "-p", "--profile", type=click.STRING, help="AWS CLI profile to use (chaim alias)"
)
@click.option(
    "-q",
    "--quiet",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="be very quiet, only show the tar file name",
)
@click.option("-s", "--start", type=click.STRING, help="optional start time")
@click.option(
    "-v",
    "--verbose",
    type=click.BOOL,
    is_flag=True,
    default=False,
    help="show files that are being copied",
)
@click.argument("path")
def star(
    compression,
    start,
    end,
    length,
    name,
    output,
    path,
    profile,
    quiet,
    usemodified,
    verbose,
):
    """Generates a tar archive of S3 files.

    Files are selected by a path made up of 'bucket/prefix'
    and optionaly by a time-based and/or name filter.

    'profile' is the AWS CLI profile to use for accessing S3.  If you use
    chaim or cca then this is the alias name for the account.

    The time based filter relies on the files being named with ISO Formatted
    dates and times embedded in the file names.  i.e.  'file.2020-03-04T12:32:21.txt'
    The regular expression used is:

        /.*[._-]{1}([0-9-]{10}T[0-9:]{8}).*/

    The 'start' and 'end' parameters can either be ISO formatted date strings
    or unix timestamps.  If only the date portion of the date/time string is given
    the time defaults to midnight of that day.

    The length parameter is a string of the form '3h', '2d', '1w' for,
    respectively 3 hours, 2 days or 1 week.  Only hours, days or weeks are
    supported.  The 'length' and 'end' parameters are mutually exclusive, give
    one or the other, not both.

    If neither the 'end' nor the 'length' parameter is given, the end time
    defaults to 'now'.

    If the 'start' parameter is not given no time filtering of the files is
    performed, and all files found down the path are copied across
    to the tar archive recursively.

    To use the last modified time stamp of the files rather than their names
    for filtering pass the '-M' flag.

    To use the name filter, pass in a partial string that object names must contain.

    The tar archive can be compressed using gzip, bzip2 or lzma. Defaults to gzip.
    Pass a one char string to the `-c` option of "g", "b", "z" or "n". "n" is
    no compression. The output tar archive will be named accordingly:
    ".tar.gz" for gzip, ".tar.bz2" for bzip2, ".tar.xz" for lzma and ".tar" for
    no compression.

    The output filename of the tar archive will be $HOME/<bucket name>.tar
    You can change this with the "-o" option.

    Using the "-q" switch will turn off all messages (except errors) apart from
    the final output of the full path of the tar archive that is created.

    Using the "-v" switch will make the program verbose, showing each file
    that is copied into the tar archive.
    """
    if not quiet:
        print(f"star {__version__}")
    uri = buildUriFromPath(path)
    sts = makeTsFromStr(start) if start is not None else 0
    dsts = displayTS(sts)
    ets = makeTsFromStr(end) if end is not None else int(time.time())
    if length is not None:
        ets = makeTsFromLength(length, sts)
    dets = displayTS(ets)
    s3 = S3FileSystem(profile=profile)
    scheme, bucket, opath = s3.parseS3Uri(uri)
    ftype = "last updated between" if usemodified else "named between"
    msg = f"Will search s3://{bucket}/{opath} for files {ftype} {dsts} and {dets}"
    if start is None:
        msg = f"will search s3://{bucket}/{opath} for all files"
    if name is not None:
        msg += f" that contain {name}"
    if not quiet:
        print(msg)
    s3.bucket = bucket
    objs, paths = s3.xls(opath)
    if len(objs) > 0:
        objects = filterObjs(objs, sts, ets, name, usemodified)
    if not quiet:
        print(f"found {len(objects)} files")
    td = tempfile.mkdtemp()
    copied = 0
    ignored = 0
    for obj in objects:
        if "StorageClass" in obj and obj["StorageClass"] in ["GLACIER", "DEEP_ARCHIVE"]:
            if not quiet:
                print(f"Not copying {src} as it is Glacier")
            ignored += 1
            continue
        src = f"""s3://{bucket}/{objects[obj]["Key"]}"""
        dest = f"""{td}/{os.path.basename(objects[obj]["Key"])}"""
        if verbose and not quiet:
            print(f"""{src} -> {dest}""")
        s3.xcp(src, dest)
        copied += 1

    cwd = os.getcwd()
    os.chdir(td)
    if compression is None:
        compression = "g"
    if compression == "n":
        ext = "tar"
        wt = "w"
    elif compression == "b":
        ext = "tar.bz2"
        wt = "w:bz2"
    elif compression == "z":
        ext = "tar.xz"
        wt = "w:xz"
    else:
        ext = "tar.gz"
        wt = "w:gz"
    home = os.environ.get("HOME", "/tmp")
    if output is None:
        output = f"{home}/{bucket}"
    elif not output.startswith("/"):
        output = f"{cwd}/{output}"
    tfn = f"{output}.{ext}"
    xtfn = tarfile.open(tfn, wt)
    for fn in glob.iglob("*"):
        xtfn.add(fn)
    xtfn.close()
    os.chdir(cwd)
    shutil.rmtree(td)
    if not quiet:
        print(f"copied: {copied}")
        print(f"ignored: {ignored}")
    print(tfn)
