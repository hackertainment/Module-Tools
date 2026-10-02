#!/usr/bin/python3

import os
import stat
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

DIR, EXT = os.environ["LS_COLORS"].replace(":*", "\n", 1).split("\n")
DIRS = dict((dir.split("=")[0],"\x1b["+dir.split("=")[1]+"m") for dir in (DIR.split(":")))
EXTS = dict((ext.split("=")[0],"\x1b["+ext.split("=")[1]+"m") for ext in (EXT[:-1].split(":")))

# add ANSI color code (and single quotes too if filename has space) to filenames
def list_pretty(path, filename, leading_space):
    filepath = os.path.join(path, filename)
    lstats = os.lstat(filepath)
    is_exist = os.path.exists(filepath)
    #link_to = "";
    #let linkColor = DIRS.rs;
    #prefix = "";
    #suffix = "";

    # if the file is a symlink, color the files they point to
    #if (isLong && lstats.isSymbolicLink()) {
    #    linkTo = fs.readlinkSync(path+"/"+filename);
    #    linkColor = (isExist ? calColorCode(traverseLink(path, filename), !fs.lstatSync(path+"/"+linkTo).isSymbolicLink()) : (DIRS.hasOwnProperty("mi") ? DIRS.mi : DIRS.rs));
    #}

    ansi_color = DIRS["rs"]

    if stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o1000)!=0 and (lstats.st_mode&0o0002)!=0:  # sticky other-writable directory (+t,o+w)
        ansi_color = DIRS["tw"] if "tw" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o0002)!=0:  # other-writable directory (o+w)
        ansi_color = DIRS["ow"] if "ow" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o1000)!=0:  # sticky directory (+t)
        ansi_color = DIRS["st"] if "st" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode):  # directory
        ansi_color = DIRS["di"] if "di" in DIRS else DIRS["rs"]
    elif stat.S_ISLNK(lstats.st_mode) and is_exist:  # symbolic link
        ansi_color = DIRS["ln"] if "ln" in DIRS else DIRS["rs"]
    elif stat.S_ISLNK(lstats.st_mode) and not is_exist:  # orphan symlink -> missing file
        ansi_color = DIRS["or"] if "or" in DIRS else DIRS["rs"]  # -> ansi_color = DIRS["mi"] if "mi" in DIRS else DIRS["rs"]
    elif stat.S_ISFIFO(lstats.st_mode):  # FIFO (named pipe)
        ansi_color = DIRS["pi"] if "pi" in DIRS else DIRS["rs"]
    elif stat.S_ISSOCK(lstats.st_mode):  # socket
        ansi_color = DIRS["so"] if "so" in DIRS else DIRS["rs"]
    elif stat.S_ISDOOR(lstats.st_mode):  # door (Solaris 2.5 and later)
        ansi_color = DIRS["du"] if "du" in DIRS else DIRS["rs"]
    elif stat.S_ISBLK(lstats.st_mode):  # block device
        ansi_color = DIRS["bd"] if "bd" in DIRS else DIRS["rs"]
    elif stat.S_ISCHR(lstats.st_mode):  # character device
        ansi_color = DIRS["cd"] if "cd" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode) and (lstats.st_mode&0o4000)!=0:  # set user id (u+s)
        ansi_color = DIRS["su"] if "su" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode) and (lstats.st_mode&0o2000)!=0:  # set group id (g+s)
        ansi_color = DIRS["sg"] if "sg" in DIRS else DIRS["rs"]
    #elif stat.S_ISREG(lstats) and ???) {  # TODO: file with capability
    #    ansi_color = DIRS["ca"] if "ca" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode) and (lstats.st_mode&0o0111)!=0:  # executable file
        ansi_color = DIRS["ex"] if "ex" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode) and ("*"+os.path.splitext(filepath)[1] in EXTS): ############### and isCheckExt) {
        ansi_color = EXTS["*"+os.path.splitext(filepath)[1]]
    elif stat.S_ISREG(lstats.st_mode) and lstats.st_nlink>1:  # multi-hardlink
        ansi_color = DIRS["mh"] if "mh" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode):  # regular file
        ansi_color = DIRS["fi"] if "fi" in DIRS else DIRS["rs"]
    else:  # normal (non-filename) text
        ansi_color = DIRS["no"] if "no" in DIRS else DIRS["rs"]

    #// if long listing format, prepend the file status details (and also append -> for symlink)
    #if (isLong) {
    #    filename = `${lstats.blocks}\t${lstats.mode}\t${lstats.nlink}\t${lstats.uid}\t${lstats.gid}\t${lstats.size}\t${lstats.mtime}\t${filename}`;
    #    if (lstats.isSymbolicLink()) {
    #        linkTo = (linkTo.includes(" ") ? "'" : "")+linkTo+(linkTo.includes(" ") ? "'" : "");
    #        filename = filename+" -> "+linkColor+linkTo+DIRS.rs;
    #    }
    #}

    return ansi_color+filename+DIRS["rs"] if " " not in filename else ansi_color+"'"+filename+"'"+DIRS["rs"]

def list_single(path, filenames):
    for row in filenames:
        print(list_pretty(path, row, ""))

# separate files from dirs (by storing filenames under an imaginary directory ""), and sort the directory names
fileArgs = []
i = 0
while i<len(paths):
    if os.path.isdir(paths[i]):
        i += 1
    elif os.path.lexists(paths[i]):
        fileArgs.append(paths.pop(i))
    else:
        print(TOOL_NAME+": cannot access '"+paths.pop(i)+"': No such file or directory")
paths.sort()
if len(fileArgs)>0:
    paths.insert(0, "")

# list filenames for each directory
for j, path in enumerate(paths):
    filenames = os.listdir(path) if path!="" else fileArgs
    is_leading_space = False

    # sort filenames, include/exclude hidden files, and set flag when any filename has space
    filenames.sort()
    if path!="":
        if is_all:
            filenames.insert(0, "..")
            filenames.insert(0, ".")
        else:
            while len(filenames)>0 and filenames[0].startswith("."):
                filenames.pop(0)
    is_leading_space = any(" " in filename for filename in filenames)

    # print filenames based on options
    if len(paths)>1 and path!="":
        print(path+":")
    if is_long:
        print(filenames)
    elif is_single:
        list_single(path, filenames)
    else:
        #column_config = cal_col_config(filenames, leading_space)
        #list_tabular(filenames, leading_space, column_config)
        print(filenames)
    if j<(len(paths)-1):
        print()