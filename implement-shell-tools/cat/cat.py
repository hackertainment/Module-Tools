#!/usr/bin/python3

import re
import argparse
import sys

TOOL_NAME = sys.argv[0].rsplit("/", 1)[1]
TOOL_AUTHOR = "Wyatt L."
TOOL_VERSION = "%s (CYF shelltools) 1.00\n\nWritten by %s" % (TOOL_NAME, TOOL_AUTHOR)
TOOL_CAVEAT = '''
Examples:
  '''+TOOL_NAME+''' f - g  Output f's contents, then standard input, then g's contents.
  '''+TOOL_NAME+'''        Copy standard input to standard output.
'''

parser = argparse.ArgumentParser(
    prog=TOOL_NAME,
    usage="%s [OPTION]... [FILE]..." % (TOOL_NAME),
    description='''
Concatenate FILE(s) to standard output.

With no FILE, or when FILE is -, read standard input.
''',
    epilog=TOOL_CAVEAT,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("-b", "--number-nonblank", action="store_true", help="number nonempty output lines, overrides -n")
parser.add_argument("-n", "--number", action="store_true", help="number all output lines")
parser.add_argument("--help", action="help", help="display this help and exit")
parser.add_argument("--version", action="version", help="output version information and exit", version=TOOL_VERSION)
parser.add_argument("FILE", nargs="*", default=["-"])
args = parser.parse_args()

files = args.FILE
is_nonblank = args.number_nonblank
is_number = False if is_nonblank else args.number

is_newline = True
count = 0

for file in files:
    try:
        with open(file if file!="-" else "/dev/stdin", "r", encoding="utf-8") as f:
            for line in f:
                if (is_number or (is_nonblank and line.rstrip("\n")!="")) and is_newline:
                    count = count+1
                    print("%6d  " % count, end="")
                print(line, end="")
                is_newline = line.endswith("\n")
    except Exception as error:
        print(re.sub("\[.*?\]", TOOL_NAME+": "+file+":", str(error).split(":")[0]))
        is_newline = False if count!=0 else True