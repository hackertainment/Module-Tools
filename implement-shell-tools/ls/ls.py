#!/usr/bin/python3

import re
import argparse
import sys

TOOL_NAME = sys.argv[0].rsplit("/", 1)[1]
TOOL_AUTHOR = "Wyatt L."
TOOL_VERSION = "%s (CYF shelltools) 1.00\n\nWritten by %s" % (TOOL_NAME, TOOL_AUTHOR)
TOOL_CAVEAT = '''
The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).
Binary prefixes can be used, too: KiB=K, MiB=M, and so on.

The TIME_STYLE argument can be full-iso, long-iso, iso, locale, or +FORMAT.
FORMAT is interpreted like in date(1).  If FORMAT is FORMAT1<newline>FORMAT2,
then FORMAT1 applies to non-recent files and FORMAT2 to recent files.
TIME_STYLE prefixed with 'posix-' takes effect only outside the POSIX locale.
Also the TIME_STYLE environment variable sets the default style to use.

Using color to distinguish file types is disabled both by default and
with --color=never.  With --color=auto, ${TOOL_NAME} emits color codes only when
standard output is connected to a terminal.  The LS_COLORS environment
variable can change the settings.  Use the dircolors command to set it.

Exit status:
 0  if OK,
 1  if minor problems (e.g., cannot access subdirectory),
 2  if serious trouble (e.g., cannot access command-line argument).
'''

parser = argparse.ArgumentParser(
    prog=TOOL_NAME,
    usage="%s [OPTION]... [FILE]..." % (TOOL_NAME),
    description='''
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
''',
    epilog=TOOL_CAVEAT,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("-a", "--all", action="store_true", help="do not ignore entries starting with .")
parser.add_argument("-l", dest="long", action="store_true", help="use a long listing format")
parser.add_argument("-1", dest="single", action="store_true", help="list one file per line.  Avoid '\\n' with -q or -b")
parser.add_argument("--help", action="help", help="display this help and exit")
parser.add_argument("--version", action="version", help="output version information and exit", version=TOOL_VERSION)
parser.add_argument("FILE", nargs="*", default=["./"])
args = parser.parse_args()

paths = args.FILE
is_all = args.all
is_long = args.long
is_single = args.single

print(args)