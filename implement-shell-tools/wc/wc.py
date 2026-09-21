#!/usr/bin/python3

import re
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
parser.add_argument("FILE", nargs="*", default=[""])
args = parser.parse_args()

files = args.FILE
is_byte = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.bytes
is_char = False if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.chars
is_word = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.words
is_line = True if args.bytes==False and args.chars==False and args.words==False and args.lines==False else args.lines

counts = {"line":0, "word":0, "char":0, "byte":0}
totals = {"line":0, "word":0, "char":0, "byte":0}
pad_size = 7  # default padding size when any file is stdin
content = ""

def count(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
            counts["line"] = content.count("\n")
            counts["word"] = len(re.findall("\S+", content))
            counts["char"] = len(content)
            counts["byte"] = len(content.encode("utf-8"))
    except Exception as error:
        raise

# prepare padding size when no file is stdin
if ("-" not in files) and ("" not in files):
    for file in files:
        try:
            count(file)
            totals = {key: totals[key]+counts[key] for key in totals}  # totals[____] += counts[____]
        except Exception as error:
            pass #print(re.sub("\[.*?\]", TOOL_NAME+": "+file+":", str(error).split(":")[0]))
    pad_size = 0
    if is_line and (len(str(totals["line"]))>pad_size):
        pad_size = len(str(totals["line"]))
    if is_word and (len(str(totals["word"]))>pad_size):
        pad_size = len(str(totals["word"]))
    if is_char and (len(str(totals["char"]))>pad_size):
        pad_size = len(str(totals["char"]))
    if is_byte and (len(str(totals["byte"]))>pad_size):
        pad_size = len(str(totals["byte"]))
    totals = {key: 0 for key in totals}  # totals[____] = 0

# count and print each file including stdin
for file in files:
    try:
        count(file if (file!="-" and file!="") else "/dev/stdin")
        totals = {key: totals[key]+counts[key] for key in totals}  # totals[____] += counts[____]
        if is_line:
            print(str(counts["line"]).rjust(pad_size, " ")+ " ", end="")
        if is_word:
            print(str(counts["word"]).rjust(pad_size, " ")+ " ", end="")
        if is_char:
            print(str(counts["char"]).rjust(pad_size, " ")+ " ", end="")
        if is_byte:
            print(str(counts["byte"]).rjust(pad_size, " ")+ " ", end="")
        print(file)
    except Exception as error:
        print(re.sub("\[.*?\]", TOOL_NAME+": "+file+":", str(error).split(":")[0]))
if len(files)>1:
    if is_line:
        print(str(totals["line"]).rjust(pad_size, " ")+ " ", end="")
    if is_word:
        print(str(totals["word"]).rjust(pad_size, " ")+ " ", end="")
    if is_char:
        print(str(totals["char"]).rjust(pad_size, " ")+ " ", end="")
    if is_byte:
        print(str(totals["byte"]).rjust(pad_size, " ")+ " ", end="")
    print("total")