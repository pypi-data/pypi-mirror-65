# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3tar']

package_data = \
{'': ['*']}

install_requires = \
['ccaaws>=0.4.6,<0.5.0', 'click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['star = s3tar.star:star']}

setup_kwargs = {
    'name': 's3tar',
    'version': '1.3.2',
    'description': 'Pulls (filtered) files from S3 and adds them to a tar archive.',
    'long_description': '# s3tar\nPulls (filtered) files from S3 and adds them to a tar archive.\n\nCreates the command line script `star`.\n\n```\n$ star --help\n\nUsage: star [OPTIONS] PATH\n\n  Generates a tar archive of S3 files.\n\n  Files are selected by a path made up of \'bucket/prefix\' and optionaly by a\n  time-based and/or name filter.\n\n  \'profile\' is the AWS CLI profile to use for accessing S3.  If you use\n  chaim or cca then this is the alias name for the account.\n\n  The time based filter relies on the files being named with ISO Formatted\n  dates and times embedded in the file names.  i.e.\n  \'file.2020-03-04T12:32:21.txt\' The regular expression used is:\n\n      /.*[._-]{1}([0-9-]{10}T[0-9:]{8}).*/\n\n  The \'start\' and \'end\' parameters can either be ISO formatted date strings\n  or unix timestamps.  If only the date portion of the date/time string is\n  given the time defaults to midnight of that day.\n\n  The length parameter is a string of the form \'3h\', \'2d\', \'1w\' for,\n  respectively 3 hours, 2 days or 1 week.  Only hours, days or weeks are\n  supported.  The \'length\' and \'end\' parameters are mutually exclusive, give\n  one or the other, not both.\n\n  If neither the \'end\' nor the \'length\' parameter is given, the end time\n  defaults to \'now\'.\n\n  If the \'start\' parameter is not given no time filtering of the files is\n  performed, and all files found down the path are copied across to the tar\n  archive recursively.\n\n  To use the last modified time stamp of the files rather than their names\n  for filtering pass the \'-M\' flag.\n\n  To use the name filter, pass in a partial string that object names must\n  contain.\n\n  The tar archive can be compressed using gzip, bzip2 or lzma. Defaults to\n  gzip. Pass a one char string to the `-c` option of "g", "b", "z" or "n".\n  "n" is no compression. The output tar archive will be named accordingly:\n  ".tar.gz" for gzip, ".tar.bz2" for bzip2, ".tar.xz" for lzma and ".tar"\n  for no compression.\n\n  The output filename of the tar archive will be $HOME/<bucket name>.tar\n  You can change this with the "-o" option.\n\n  Using the "-q" switch will turn off all messages (except errors) apart\n  from the final output of the full path of the tar archive that is created.\n\n  Using the "-v" switch will make the program verbose, showing each file\n  that is copied into the tar archive.\n\n  Files in Glacier and Glacier Deep Archive are ignored.\n\nOptions:\n  -c, --compression TEXT  optional compression [\'b\', \'g\', \'n\', \'z\'], default\n                          \'g\'\n\n  -e, --end TEXT          optional end time\n  -l, --length TEXT       optional time length (i.e. 1d, 3h, 4w)\n  -M, --usemodified       use last modified time stamp rather than filename\n                          for filtering\n\n  -N, --name TEXT         optional name filter\n  -o, --output TEXT       output file name (default: bucket name)\n  -p, --profile TEXT      AWS CLI profile to use (chaim alias)\n  -q, --quiet             be very quiet, only show the tar file name\n  -s, --start TEXT        optional start time\n  -v, --verbose           show files that are being copied\n  --help                  Show this message and exit.\n\n```\n\n## Install\nThe script is python3 only (>=python3.6).\n\nInstall it under your python3 user directories with:\n\n```\npython3 -m pip install s3tar --user\n```\n\nIf this is the first python3 user script you have you will have to adjust\nyour path.  The script location will be `$HOME/.local/bin` on a Linux\nmachine, so add that to you path in your shell init file e.g.\n\n```\necho "export PATH=$HOME/.local/bin:$PATH" >>~/.bashrc\n```\n\nIf your shell is bash.\n\nTo check that installed ok:\n\n```\nstar --help\n```\n\nShould display the help text.\n',
    'author': 'Chris Allison',
    'author_email': 'chris.charles.allison+s3tar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/s3tar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
