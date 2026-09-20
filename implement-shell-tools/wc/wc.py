#!/usr/bin/python3

import argparse
import sys

TOOL_NAME = sys.argv[0].rsplit("/", 1)[1]
TOOL_AUTHOR = "Wyatt L."
TOOL_VERSION = "%s (CYF shelltools) 1.00\n\nWritten by %s" % (TOOL_NAME, TOOL_AUTHOR)
TOOL_CAVEAT = ""

parser = argparse.ArgumentParser(
    prog=TOOL_NAME,
    usage="%s [OPTION]... [FILE]...\n  or:  %s [OPTION]... --files0-from=F" % (TOOL_NAME, TOOL_NAME),
    description='''
Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  A word is a non-zero-length sequence of
characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.
''',
    epilog=TOOL_CAVEAT,
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
parser.add_argument("--help", action="help", help="display this help and exit")
parser.add_argument("--version", action="version", help="output version information and exit", version=TOOL_VERSION)
parser.add_argument("FILE", nargs="*", default=["-"])
args = parser.parse_args()

print(args)
files = args.FILE
is_byte = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.bytes
is_char = False if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.chars
is_word = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.words
is_line = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.lines
print(is_byte, is_char, is_word, is_line, files)