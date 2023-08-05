# s3tar
Pulls (filtered) files from S3 and adds them to a tar archive.

Creates the command line script `star`.

```
$ star --help
Usage: star [OPTIONS] PATH

  Generates a tar archive of S3 files.

  Files are selected by a path made up of 'bucket/prefix' and optionaly by a
  time-based filter.

  'profile' is the AWS CLI profile to use for accessing S3.  If you use
  chaim or cca then this is the alias name for the account.

  The time based filter relies on the files being named with ISO Formatted
  dates and times embedded in the file names.  i.e.
  'file.2020-03-04T12:32:21.txt' The regular expression used is:

      /.*[._-]{1}([0-9-]{10}T[0-9:]{8}).*/

  The 'start' and 'end' parameters can either be ISO formatted date strings
  or unix timestamps.  If only the date portion of the date/time string is
  given the time defaults to midnight of that day.

  The length parameter is a string of the form '3h', '2d', '1w' for,
  respectively 3 hours, 2 days or 1 week.  Only hours, days or weeks are
  supported.  The 'length' and 'end' parameters are mutually exclusive, give
  one or the other, not both.

  If neither the 'end' nor the 'length' parameter is given, the end time
  defaults to 'now'.

  If the 'start' parameter is not given no filtering of the files is
  performed, and all files found down the path are copied across to the tar
  archive recursively.

Options:
  -e, --end TEXT      optional end time
  -l, --length TEXT   optional time length (i.e. 1d, 3h, 4w)
  -p, --profile TEXT  AWS CLI profile to use (chaim alias)
  -s, --start TEXT    optional start time
  --help              Show this message and exit.
```
