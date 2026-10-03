#!/usr/bin/python3

import os
import stat
import math
import datetime
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
with --color=never.  With --color=auto, '''+TOOL_NAME+''' emits color codes only when
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

def init_terminal_info():
    # `ls` uses an environment variable, COLUMNS, to determine the number of character positions available on one output line.
    # If this variable is not set, the `terminfo(4)` database is used to determine the number of columns, based on the environment variable, TERM.
    # If this information cannot be obtained, 80 columns are assumed.
    if "COLUMNS" in os.environ:
        return os.environ["COLUMNS"]
    try:
        return os.get_terminal_size().columns
    except OSError as error:
        return 80

def init_entries(filepath):
    lines = []
    fields = []
    ids = {}

    with open(filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip()!="" and line.strip()[0]!="#":
                fields = line.strip().split(":")
                ids[str(fields[2])] = fields[0]

    return ids

DIR, EXT = os.environ["LS_COLORS"].replace(":*", "\n", 1).split("\n")
DIRS = dict((dir.split("=")[0],"\x1b["+dir.split("=")[1]+"m") for dir in (DIR.split(":")))
EXTS = dict((ext.split("=")[0],"\x1b["+ext.split("=")[1]+"m") for ext in (EXT[:-1].split(":")))
UIDS = init_entries("/etc/passwd")
GIDS = init_entries("/etc/group")
CHRS = init_terminal_info()+1

# https://askubuntu.com/a/884513
# https://talyian.github.io/ansicolors/
# apply ANSI color code (and maybe leading space or single quotes) to a filename
def format_pretty(path, filename, is_leading_space, is_check_ext):
    filepath = os.path.join(path, filename)
    lstats = os.lstat(filepath) if os.path.lexists(filepath) else None
    ansi_color = DIRS["rs"]

    if lstats is None:  # missing file
        ansi_color = DIRS["mi"] if "mi" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o1000)!=0 and (lstats.st_mode&0o0002)!=0:  # sticky other-writable directory (+t,o+w)
        ansi_color = DIRS["tw"] if "tw" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o0002)!=0:  # other-writable directory (o+w)
        ansi_color = DIRS["ow"] if "ow" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode) and (lstats.st_mode&0o1000)!=0:  # sticky directory (+t)
        ansi_color = DIRS["st"] if "st" in DIRS else DIRS["rs"]
    elif stat.S_ISDIR(lstats.st_mode):  # directory
        ansi_color = DIRS["di"] if "di" in DIRS else DIRS["rs"]
    elif stat.S_ISLNK(lstats.st_mode) and os.path.exists(filepath):  # symbolic link
        ansi_color = DIRS["ln"] if "ln" in DIRS else DIRS["rs"]
    elif stat.S_ISLNK(lstats.st_mode) and not os.path.exists(filepath):  # orphan symlink -> missing file
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
    elif stat.S_ISREG(lstats.st_mode) and ("*"+os.path.splitext(filepath)[1] in EXTS) and is_check_ext:
        ansi_color = EXTS["*"+os.path.splitext(filepath)[1]]
    elif stat.S_ISREG(lstats.st_mode) and lstats.st_nlink>1:  # multi-hardlink
        ansi_color = DIRS["mh"] if "mh" in DIRS else DIRS["rs"]
    elif stat.S_ISREG(lstats.st_mode):  # regular file
        ansi_color = DIRS["fi"] if "fi" in DIRS else DIRS["rs"]
    else:  # normal (non-filename) text
        ansi_color = DIRS["no"] if "no" in DIRS else DIRS["rs"]

    if " " in filename:
        filename = ansi_color+"'"+filename+"'"+DIRS["rs"]
    elif is_leading_space:
        filename = " "+ansi_color+filename+DIRS["rs"]
    else:
        filename = ansi_color+filename+DIRS["rs"]

    return filename

def list_single(path, filenames):
    for row in filenames:
        print(format_pretty(path, row, False, True))

# https://stackoverflow.com/a/50841264
# https://www.unix.com/man-page/opensolaris/1/ls/
def file_xattr():
    return "."  # TODO: "@" else "+" else "."

def traverse_link(path, symlink):
    filepath = os.path.join(path, symlink)

    if os.path.islink(filepath):
        if "/" in symlink:
            path = os.path.dirname(filepath)
        symlink = os.readlink(filepath)
        filepath = traverse_link(path, symlink)

    return filepath

def list_long(path, filenames, is_leading_space):
    filepath = None
    lstats = None
    rows = []

    cols = []
    total_block = 0
    max_nlink = 0
    max_ulength = 0
    max_glength = 0
    max_size = 0
    length = 0

    link_to = ""
    link_color = DIRS["rs"]

    # calculate width of columns
    for i, filename in enumerate(filenames):
        filepath = os.path.join(path, filename)
        lstats = os.lstat(filepath)
        rows.append(str(lstats.st_blocks)+"\t"+str(lstats.st_mode)+"\t"+str(lstats.st_nlink)+"\t"+str(lstats.st_uid)+"\t"+str(lstats.st_gid)+"\t"+str(lstats.st_size)+"\t"+str(lstats.st_mtime)+"\t")
        if stat.S_ISLNK(lstats.st_mode):
            rows[i] = rows[i]+os.readlink(filepath)

        total_block = total_block+lstats.st_blocks
        max_nlink = lstats.st_nlink if lstats.st_nlink>max_nlink else max_nlink
        length = len(UIDS[str(lstats.st_uid)])
        max_ulength = length if length>max_ulength else max_ulength
        length = len(GIDS[str(lstats.st_gid)])
        max_glength = length if length>max_glength else max_glength
        max_size = lstats.st_size if lstats.st_size>max_size else max_size

    # https://unix.stackexchange.com/questions/28780/file-block-size-difference-between-stat-and-ls
    # linux `stat` struct stat {... blkcnt_t  st_blocks; ...} indicates *number of 512B blocks allocated*
    # but `ls` #define DEFAULT_BLOCK_SIZE 1024 *Byte*
    # so for example 9-10 blocks in `stat` would just be 5 blocks in `ls`
    print("total", math.ceil(total_block/2))
    for j, row in enumerate(rows):
        cols = row.split("\t")
        print(stat.filemode(int(cols[1]))+file_xattr(), end=" ")
        print(("%"+str(len(str(max_nlink)))+"s") % cols[2], end=" ")
        print(("%"+str(max_ulength)+"s") % UIDS[cols[3]], end=" ")
        print(("%"+str(max_glength)+"s") % GIDS[cols[4]], end=" ")
        print(("%"+str(len(str(max_size)))+"s") % cols[5], end=" ")
        print(datetime.datetime.fromtimestamp(float(cols[6])).strftime("%b\t%d %H:%M").replace("\t0", "  ").replace("\t", " "), end=" ")
        print(format_pretty(path, filenames[j], is_leading_space, True), end="")
        if cols[7]!="":
            if os.path.islink(os.path.join(path, cols[7])):  # if it is a link to another symlink
                # then traverse the link to determine color (except extension check) first, and then replace display text back by cols[7] afterwards
                linked_to = traverse_link(path, filenames[j])
                linked_color = format_pretty(path, linked_to, False, False)
                linked_to = "'"+linked_to+"'" if " " in linked_to else linked_to
                cols[7] = linked_color.replace(linked_to, cols[7])
            else:  # else it can be a direct link to file/directory (need extension check) or a broken link to missing
                cols[7] = format_pretty(path, cols[7], False, True)
            print(" -> "+cols[7], end="")
        print()

# https://stackoverflow.com/a/75575528/8842262
# https://mmzeynalli.dev/posts/reinvent/ls/part5/#3-tabular
def config_column(filenames, num_space):
    max_num_col = math.floor(CHRS/3)  # filename minimum 1 char + 2 spaces = 3
    max_widths = [[0]]
    col = 0
    sum = 0
    widths = []

    for j in range(len(filenames)):
        widths.append(len(filenames[j])+(2+2 if " " in filenames[j] else num_space+2))

    #     num_col   [   0     ,    1     ,    2     , ...]
    #        0    =    ???
    #        1    = [max_width]
    #        2    = [max_width, max_width]
    #        3    = [max_width, max_width, max_width]
    #        :    = [ ...
    # max_num_col = [ ...
    max_num_col = len(filenames) if len(filenames)<=max_num_col else max_num_col
    for i in range(1, max_num_col+1):  # for each column config
        max_widths.append([3]*i)  # init config as an array of three(3)s
    for i in range(1, max_num_col+1):  # for each column config
        for j in range(len(widths)):
            col = math.floor(j/(math.ceil(len(widths)/i)))
            if widths[j]>max_widths[i][col]:  # if width > max width in that column
                max_widths[i][col] = widths[j]  # then update max width in that column
    for i in range(1, max_num_col+1):  # for each column config
        sum = 0
        for j in range(i):
            sum = sum+max_widths[i][j];  # sum all max widths
        if sum<=CHRS:  # if sum <= terminal width
            max_widths[0][0] = i  # store the index of such column config

    return max_widths[max_widths[0][0]];  # return the largest possible column config

def list_tabular(path, filenames, is_leading_space):
    pad_cols = config_column(filenames, 1 if is_leading_space else 0)
    num_pad = 0
    num_row = math.ceil(len(filenames)/len(pad_cols))
    row = ""
    index = None  # calculated index of filenames[]

    for i in range(num_row):  # for each row
        row = ""
        for j in range(len(pad_cols)):  # for each col
            index = i+num_row*j  # pick the (i+numRow*j)'th file from array for printing
            if index<len(filenames):
                num_pad = pad_cols[j]-len(filenames[index])
                if " " in filenames[index]:
                    num_pad = num_pad-2
                elif is_leading_space:
                    num_pad = num_pad-1
                row = row+format_pretty(path, filenames[index], is_leading_space, True)+(" "*num_pad)
        print(row.rstrip())

# separate files from directories (by storing filenames under an imaginary directory ""), and sort the directory names
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

    # print filenames based on command line options
    if len(paths)>1 and path!="":
        print(path+":")
    if is_long:
        list_long(path, filenames, is_leading_space)
    elif is_single:
        list_single(path, filenames)
    else:
        list_tabular(path, filenames, is_leading_space)
    if j<(len(paths)-1):
        print()