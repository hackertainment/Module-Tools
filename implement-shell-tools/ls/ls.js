#!/home/ec2-user/.nvm/versions/node/v24.19.0/bin/node

import { program } from "commander";
//import { promises as fs } from "node:fs";
import fs from "node:fs";
import process from "node:process";

const TOOL_NAME = process.argv[1].split("/").pop();
const TOOL_AUTHOR = "Wyatt L.";
const TOOL_VERSION = `${TOOL_NAME} (CYF shelltools) 1.00\n\nWritten by ${TOOL_AUTHOR}`;
const TOOL_CAVEAT = `
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
`;

program
    .name(TOOL_NAME)
    .usage("[OPTION]... [FILE]...")
    .description("List information about the FILEs (the current directory by default).\nSort entries alphabetically if none of -cftuvSUX nor --sort is specified.")
    .option("-a, --all", "do not ignore entries starting with .")
    .option("-l", "use a long listing format")
    .helpOption("--help", "display this help and exit")
    .version(TOOL_VERSION, "--version", "output version information and exit")
    .addHelpText("after", TOOL_CAVEAT)
    .argument("[FILE...]", null, ["./"])
    .parse();

const paths = program.args.sort();
const isAll = program.opts().all;
const isLong = program.opts().l;

// commander not correctly specify default value for an optional command-argument
if (paths.length==0) {
    paths.push("./");
}

const RWXS = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
const [DIR, EXT] = process.env.LS_COLORS.replace(":*", "\n").split("\n");
const DIRS = Object.fromEntries(new URLSearchParams(DIR.replaceAll("=", "=\x1b[").replaceAll(":", "m&")+"m"));
const EXTS = Object.fromEntries(new URLSearchParams(EXT.replaceAll("=", "=\x1b[").replaceAll(":", "m&")));
const UIDS = {};
const GIDS = {};

function getent() {
    let passwds = fs.readFileSync("/etc/passwd", "utf8").split("\n");
    let groups = fs.readFileSync("/etc/group", "utf8").split("\n");
    let fields = [];
    let length = 0;

    for (let line of passwds) {
        if (line.trim()!="" && !line.startsWith("#")) {
            fields = line.split(":");
            UIDS[fields[2].toString()] = fields[0];
        }
    }
    for (let line of groups) {
        if (line.trim()!="" && !line.startsWith("#")) {
            fields = line.split(":");
            GIDS[fields[2].toString()] = fields[0];
        }
    }
}

function listPretty(isPrependSpace, path) {
    return function (filename) {
        const lstats = fs.lstatSync(path+"/"+filename);
        const isExist = fs.existsSync(path+"/"+filename);
        let prefix = "";
        let suffix = "";

        // if filename has space, add single quote to it and leading space to others
        if (filename.includes(" ")) {
            prefix = "'";
            suffix = "'";
        }
        else if (isPrependSpace) {
            prefix = " ";
        }

        Object.assign(DIRS, {rs: "\x1b[0m"});
        if (lstats.isDirectory() && (lstats.mode&0o1000)!=0 && (lstats.mode&0o0002)!=0) {  // sticky other-writable directory (+t,o+w)
            filename = (DIRS.hasOwnProperty("tw") ? DIRS.tw : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isDirectory() && (lstats.mode&0o0002)!=0) {  // other-writable directory (o+w)
            filename = (DIRS.hasOwnProperty("ow") ? DIRS.ow : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isDirectory() && (lstats.mode&0o1000)!=0) {  // sticky directory (+t)
            filename = (DIRS.hasOwnProperty("st") ? DIRS.st : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isDirectory()) {  // directory
            filename = (DIRS.hasOwnProperty("di") ? DIRS.di : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isSymbolicLink() && isExist) {  // symbolic link
            filename = (DIRS.hasOwnProperty("ln") ? DIRS.ln : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isSymbolicLink() && !isExist) {  // orphan symlink -> missing file
            filename = (DIRS.hasOwnProperty("or") ? DIRS.or : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFile() && lstats.nlink>1) {  // multi-hardlink
            filename = (DIRS.hasOwnProperty("mh") ? DIRS.mh : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFIFO()) {  // FIFO (named pipe)
            filename = (DIRS.hasOwnProperty("pi") ? DIRS.pi : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isSocket()) {  // socket
            filename = (DIRS.hasOwnProperty("so") ? DIRS.so : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isSocket()) {  // door (Solaris 2.5 and later)
            filename = (DIRS.hasOwnProperty("do") ? DIRS.do : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isBlockDevice()) {  // block device
            filename = (DIRS.hasOwnProperty("bd") ? DIRS.bd : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isCharacterDevice()) {  // character device
            filename = (DIRS.hasOwnProperty("cd") ? DIRS.cd : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFile() && (lstats.mode&0o4000)!=0) {  // set user id (u+s)
            filename = (DIRS.hasOwnProperty("su") ? DIRS.su : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFile() && (lstats.mode&0o2000)!=0) {  // set group id (g+s)
            filename = (DIRS.hasOwnProperty("sg") ? DIRS.sg : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        //else if (lstats.isFile() && ???) {  // TODO: file with capability
        //    filename = (DIRS.hasOwnProperty("ca") ? DIRS.ca : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        //}
        else if (lstats.isFile() && (lstats.mode&0o0111)!=0) {  // executable file
            filename = (DIRS.hasOwnProperty("ex") ? DIRS.ex : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFile() && Object.keys(EXTS).includes("*."+filename.split(".").pop())) {
            filename = EXTS["*."+filename.split(".").pop()]+prefix+filename+suffix+DIRS.rs;
        }
        else if (lstats.isFile()) {  // regular file
            filename = (DIRS.hasOwnProperty("fi") ? DIRS.fi : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }
        else {  // normal (non-filename) text
            filename = (DIRS.hasOwnProperty("no") ? DIRS.no : DIRS.rs)+prefix+filename+suffix+DIRS.rs;
        }

        if (isLong) {
            filename = `${lstats.blocks}\t${lstats.mode}\t${lstats.nlink}\t${lstats.uid}\t${lstats.gid}\t${lstats.size}\t${lstats.mtime}\t${filename}`;
        }

        return filename;
    }
}

function listLong(prettyFilenames) {
    let cols = [];
    let totalBlock = 0;
    let maxNlink = 0;
    let maxUlength = 0;
    let maxGlength = 0;
    let maxSize = 0;
    let ftype = " ";
    let owner = "---";
    let group = "---";
    let other = "---";
    let xattr = " ";

    for (let row of prettyFilenames) {
        cols = row.split("\t");
        totalBlock = totalBlock+Number(cols[0]);
        maxNlink = (Number(cols[2])>maxNlink ? Number(cols[2]) : maxNlink);
        length = UIDS[cols[3].toString()].length;
        maxUlength = (length>maxUlength ? length : maxUlength);
        length = GIDS[cols[4].toString()].length;
        maxUlength = (length>maxGlength ? length : maxGlength);
        maxSize = (Number(cols[5])>maxSize ? Number(cols[5]) : maxSize);
    }

    // https://unix.stackexchange.com/questions/28780/file-block-size-difference-between-stat-and-ls
    // linux `stat` struct stat {... blkcnt_t  st_blocks; ...} indicates *number of 512B blocks allocated*
    // but `ls` #define DEFAULT_BLOCK_SIZE 1024 *Byte*
    // so for example 9-10 blocks in `stat` would just be 5 blocks in `ls`
    process.stdout.write("total "+Math.ceil(totalBlock/2)+"\n");
    for (let row of prettyFilenames) {
        cols = row.split("\t");
        if ((cols[1]&fs.constants.S_IFSOCK)==fs.constants.S_IFSOCK) {
            ftype = "s";  // socket
        }
        else if ((cols[1]&fs.constants.S_IFLNK)==fs.constants.S_IFLNK) {
            ftype = "l";  // symbolic link
        }
        else if ((cols[1]&fs.constants.S_IFREG)==fs.constants.S_IFREG) {
            ftype = "-";  // regular file
        }
        else if ((cols[1]&fs.constants.S_IFBLK)==fs.constants.S_IFBLK) {
            ftype = "b";  // block-oriented device file
        }
        else if ((cols[1]&fs.constants.S_IFDIR)==fs.constants.S_IFDIR) {
            ftype = "d";  // directory
        }
        else if ((cols[1]&fs.constants.S_IFCHR)==fs.constants.S_IFCHR) {
            ftype = "c";  // character-oriented device file
        }
        else if ((cols[1]&fs.constants.S_IFIFO)==fs.constants.S_IFIFO) {
            ftype = "p";  // FIFO/pipe
        }
        else if ((cols[1]&fs.constants.S_IFMT)!=0) {  // bit mask used to extract the file type code
            ftype = "D";  // door
        }
        else {
            ftype = "P";  // event port
        }
        owner = RWXS[(cols[1]>>6)&7];
        group = RWXS[(cols[1]>>3)&7];
        other = RWXS[(cols[1])&7];
        if ((cols[1]&fs.constants.S_ISUID)!=0) {
            owner = owner[0]+owner[1]+(owner[2]=="x" ? "s" : "S");
        }
        if ((cols[1]&fs.constants.S_ISGID)!=0) {
            group = group[0]+group[1]+(group[2]=="x" ? "s" : "S");
        }
        if ((cols[1]&fs.constants.S_ISVTX)!=0) {
            group = other[0]+other[1]+(other[2]=="x" ? "t" : "T");
        }
        xattr = ".";  // TODO: "@" or "+" or "."
        process.stdout.write(ftype+owner+group+other+xattr+" ");
        process.stdout.write(cols[2].toString().padStart(maxNlink.toString().length, " ")+" ");
        process.stdout.write(UIDS[cols[3].toString()].padEnd(maxUlength, " ")+" ");
        process.stdout.write(GIDS[cols[4].toString()].padEnd(maxGlength, " ")+" ");
        process.stdout.write(cols[5].toString().padStart(maxSize.toString().length, " ")+" ");
        process.stdout.write(cols[6].slice(4, 10).replace(" 0", "  ")+cols[6].slice(15, 21)+" ");
        process.stdout.write(cols[7]+"\n");
    }
}

function listTabular(prettyFilenames) {
    for (let prettyName of prettyFilenames) {
        process.stdout.write(prettyName+"  ");
    }
    process.stdout.write("\n");
}

getent();
for (let [i, path] of paths.entries()) {
    let prettyFilenames = [];
    let filenames = fs.readdirSync(path);
    let isAnySpace = filenames.filter((filename) => filename.includes(" ")).length!=0;

    filenames.sort();
    if (isAll) {
        filenames.unshift("..")
        filenames.unshift(".");
    }
    else {
        while (filenames.length>0 && filenames[0].startsWith(".")) {
            filenames.shift();
        }
    }

    prettyFilenames = filenames.map(listPretty(isAnySpace, path));  // the whole  ̲l̲i̲s̲t̲P̲r̲e̲t̲t̲y̲(̲i̲s̲A̲n̲y̲S̲p̲a̲c̲e̲,̲ ̲p̲a̲t̲h̲)̲ ̲ is a template function name
    if (paths.length>1) {
        process.stdout.write(path+":\n");
    }
    if (isLong) {
        listLong(prettyFilenames);
    }
    else {
        listTabular(prettyFilenames);
    }
    if (i<paths.length-1) {
        process.stdout.write("\n");
    }
}