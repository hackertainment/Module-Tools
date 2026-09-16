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
    .option("-1", "list one file per line.  Avoid '\\n' with -q or -b")
    .helpOption("--help", "display this help and exit")
    .version(TOOL_VERSION, "--version", "output version information and exit")
    .addHelpText("after", TOOL_CAVEAT)
    .argument("[FILE...]", null, ["./"])
    .parse();

const paths = program.args;
const isAll = program.opts().all;
const isLong = program.opts().l;
const isSingle = program.opts()["1"];

// commander not correctly specify default value for an optional command-argument
if (paths.length==0) {
    paths.push("./");
}

const [DIR, EXT] = process.env.LS_COLORS.replace(":*", "\n").split("\n");
const DIRS = Object.fromEntries(new URLSearchParams(DIR.replaceAll("=", "=\x1b[").replaceAll(":", "m&")+"m"));
const EXTS = Object.fromEntries(new URLSearchParams(EXT.replaceAll("=", "=\x1b[").replaceAll(":", "m&")));
const RWXS = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"];
const UIDS = initEntries("/etc/passwd");
const GIDS = initEntries("/etc/group");
const CHRS = initTerminalInfo()+1;

function initTerminalInfo() {
    // `ls` uses an environment variable, COLUMNS, to determine the number of character positions available on one output line.
    // If this variable is not set, the `terminfo(4)` database is used to determine the number of columns, based on the environment variable, TERM.
    // If this information cannot be obtained, 80 columns are assumed.
    if (process.env.COLUMNS!==undefined) {
        return process.env.COLUMNS;
    }
    else if (process.stdout.columns!==undefined) {
        return process.stdout.columns;
    }
    else {
        return 80;
    }
}

function initEntries(filepath) {
    let lines = [];
    let fields = [];
    let ids = {};

    lines = fs.readFileSync(filepath, "utf8").split("\n");
    for (let line of lines) {
        if (line.trim()!="" && !line.startsWith("#")) {
            fields = line.split(":");
            ids[fields[2].toString()] = fields[0];
        }
    }

    return ids;
}

function traverseLink(path, symlink) {
    let filepath = path+"/"+symlink;

    if (fs.lstatSync(filepath).isSymbolicLink()) {
        if (symlink.includes("/")) {
            path = path+symlink.slice(0, symlink.lastIndexOf("/")+1);
        }
        symlink = fs.readlinkSync(filepath);
        filepath = traverseLink(path, symlink);
    }

    return filepath;
}

// https://askubuntu.com/a/884513
// https://talyian.github.io/ansicolors/
function calColorCode(filepath, isCheckExt) {
    const lstats = fs.lstatSync(filepath);
    const isExist = fs.existsSync(filepath);
    let ansiColor = DIRS.rs;

    if (lstats.isDirectory() && (lstats.mode&0o1000)!=0 && (lstats.mode&0o0002)!=0) {  // sticky other-writable directory (+t,o+w)
        ansiColor = (DIRS.hasOwnProperty("tw") ? DIRS.tw : DIRS.rs);
    }
    else if (lstats.isDirectory() && (lstats.mode&0o0002)!=0) {  // other-writable directory (o+w)
        ansiColor = (DIRS.hasOwnProperty("ow") ? DIRS.ow : DIRS.rs);
    }
    else if (lstats.isDirectory() && (lstats.mode&0o1000)!=0) {  // sticky directory (+t)
        ansiColor = (DIRS.hasOwnProperty("st") ? DIRS.st : DIRS.rs);
    }
    else if (lstats.isDirectory()) {  // directory
        ansiColor = (DIRS.hasOwnProperty("di") ? DIRS.di : DIRS.rs);
    }
    else if (lstats.isSymbolicLink() && isExist) {  // symbolic link
        ansiColor = (DIRS.hasOwnProperty("ln") ? DIRS.ln : DIRS.rs);
    }
    else if (lstats.isSymbolicLink() && !isExist) {  // orphan symlink -> missing file
        ansiColor = (DIRS.hasOwnProperty("or") ? DIRS.or : DIRS.rs);  // -> ansiColor = (DIRS.hasOwnProperty("mi") ? DIRS.or : DIRS.rs);
    }
    else if (lstats.isFile() && lstats.nlink>1) {  // multi-hardlink
        ansiColor = (DIRS.hasOwnProperty("mh") ? DIRS.mh : DIRS.rs);
    }
    else if (lstats.isFIFO()) {  // FIFO (named pipe)
        ansiColor = (DIRS.hasOwnProperty("pi") ? DIRS.pi : DIRS.rs);
    }
    else if (lstats.isSocket()) {  // socket
        ansiColor = (DIRS.hasOwnProperty("so") ? DIRS.so : DIRS.rs);
    }
    else if (lstats.isSocket()) {  // door (Solaris 2.5 and later)
        ansiColor = (DIRS.hasOwnProperty("do") ? DIRS.do : DIRS.rs);
    }
    else if (lstats.isBlockDevice()) {  // block device
        ansiColor = (DIRS.hasOwnProperty("bd") ? DIRS.bd : DIRS.rs);
    }
    else if (lstats.isCharacterDevice()) {  // character device
        ansiColor = (DIRS.hasOwnProperty("cd") ? DIRS.cd : DIRS.rs);
    }
    else if (lstats.isFile() && (lstats.mode&0o4000)!=0) {  // set user id (u+s)
        ansiColor = (DIRS.hasOwnProperty("su") ? DIRS.su : DIRS.rs);
    }
    else if (lstats.isFile() && (lstats.mode&0o2000)!=0) {  // set group id (g+s)
        ansiColor = (DIRS.hasOwnProperty("sg") ? DIRS.sg : DIRS.rs);
    }
    //else if (lstats.isFile() && ???) {  // TODO: file with capability
    //    ansiColor = (DIRS.hasOwnProperty("ca") ? DIRS.ca : DIRS.rs);
    //}
    else if (lstats.isFile() && (lstats.mode&0o0111)!=0) {  // executable file
        ansiColor = (DIRS.hasOwnProperty("ex") ? DIRS.ex : DIRS.rs);
    }
    else if (lstats.isFile() && Object.keys(EXTS).includes("*."+filepath.split(".").pop()) && isCheckExt) {
        ansiColor = EXTS["*."+filepath.split(".").pop()];
    }
    else if (lstats.isFile()) {  // regular file
        ansiColor = (DIRS.hasOwnProperty("fi") ? DIRS.fi : DIRS.rs);
    }
    else {  // normal (non-filename) text
        ansiColor = (DIRS.hasOwnProperty("no") ? DIRS.no : DIRS.rs);
    }

    return ansiColor;
}

function listPretty(isPrependSpace, path) {
    return function (filename) {
        const lstats = fs.lstatSync(path+"/"+filename);
        const isExist = fs.existsSync(path+"/"+filename);
        let linkTo = "";
        let linkColor = DIRS.rs;
        let prefix = "";
        let suffix = "";

        // if a filename has space, add single quote to it and leading space to others
        if (filename.includes(" ")) {
            prefix = "'";
            suffix = "'";
        }
        else if (isPrependSpace) {
            prefix = " ";
        }

        // if the file is a symlink, color the files they point to
        if (isLong && lstats.isSymbolicLink()) {
            linkTo = fs.readlinkSync(path+"/"+filename);
            linkColor = (isExist ? calColorCode(traverseLink(path, filename), !fs.lstatSync(path+"/"+linkTo).isSymbolicLink()) : (DIRS.hasOwnProperty("mi") ? DIRS.mi : DIRS.rs));
        }

        // PRETTY THE FILENAME
        filename = calColorCode(path+"/"+filename, true)+prefix+filename+suffix+DIRS.rs;
        
        // if long listing format, prepend the file status details (and also append -> for symlink)
        if (isLong) {
            filename = `${lstats.blocks}\t${lstats.mode}\t${lstats.nlink}\t${lstats.uid}\t${lstats.gid}\t${lstats.size}\t${lstats.mtime}\t${filename}`;
            if (lstats.isSymbolicLink()) {
                linkTo = (linkTo.includes(" ") ? "'" : "")+linkTo+(linkTo.includes(" ") ? "'" : "");
                filename = filename+" -> "+linkColor+linkTo+DIRS.rs;
            }
        }

        return filename;
    }
}

// https://stackoverflow.com/a/50841264
// https://www.unix.com/man-page/opensolaris/1/ls/
function calCharFlag(mode) {
    let ftype = " ";
    let owner = "---";
    let group = "---";
    let other = "---";
    let xattr = " ";

    if ((mode&fs.constants.S_IFSOCK)==fs.constants.S_IFSOCK) {
        ftype = "s";  // socket
    }
    else if ((mode&fs.constants.S_IFLNK)==fs.constants.S_IFLNK) {
        ftype = "l";  // symbolic link
    }
    else if ((mode&fs.constants.S_IFREG)==fs.constants.S_IFREG) {
        ftype = "-";  // regular file
    }
    else if ((mode&fs.constants.S_IFBLK)==fs.constants.S_IFBLK) {
        ftype = "b";  // block-oriented device file
    }
    else if ((mode&fs.constants.S_IFDIR)==fs.constants.S_IFDIR) {
        ftype = "d";  // directory
    }
    else if ((mode&fs.constants.S_IFCHR)==fs.constants.S_IFCHR) {
        ftype = "c";  // character-oriented device file
    }
    else if ((mode&fs.constants.S_IFIFO)==fs.constants.S_IFIFO) {
        ftype = "p";  // FIFO/pipe
    }
    else if ((mode&fs.constants.S_IFMT)!=0) {  // bit mask used to extract the file type code
        ftype = "D";  // door
    }
    else {
        ftype = "P";  // event port
    }
    owner = RWXS[(mode&fs.constants.S_IRWXU)>>6];
    group = RWXS[(mode&fs.constants.S_IRWXG)>>3];
    other = RWXS[mode&fs.constants.S_IRWXO];
    if ((mode&fs.constants.S_ISUID)!=0) {
        owner = owner[0]+owner[1]+(owner[2]=="x" ? "s" : "S");
    }
    if ((mode&fs.constants.S_ISGID)!=0) {
        group = group[0]+group[1]+(group[2]=="x" ? "s" : "S");
    }
    if ((mode&fs.constants.S_ISVTX)!=0) {
        group = other[0]+other[1]+(other[2]=="x" ? "t" : "T");
    }
    xattr = ".";  // TODO: "@" else "+" else "."

    return (ftype+owner+group+other+xattr);
}

function listLong(prettyFilenames) {
    let cols = [];
    let totalBlock = 0;
    let maxNlink = 0;
    let maxUlength = 0;
    let maxGlength = 0;
    let maxSize = 0;
    let length = 0;

    // calculate width of columns
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
        process.stdout.write(calCharFlag(cols[1])+" ");
        process.stdout.write(cols[2].toString().padStart(maxNlink.toString().length, " ")+" ");
        process.stdout.write(UIDS[cols[3].toString()].padEnd(maxUlength, " ")+" ");
        process.stdout.write(GIDS[cols[4].toString()].padEnd(maxGlength, " ")+" ");
        process.stdout.write(cols[5].toString().padStart(maxSize.toString().length, " ")+" ");
        process.stdout.write(cols[6].slice(4, 10).replace(" 0", "  ")+cols[6].slice(15, 21)+" ");
        process.stdout.write(cols[7]+"\n");
    }
}

function listSingle(prettyFilenames) {
    for (let row of prettyFilenames) {
        process.stdout.write(row+"\n");
    }
}

// https://stackoverflow.com/a/75575528/8842262
// https://mmzeynalli.dev/posts/reinvent/ls/part5/#3-tabular
function calColConfig(filenames, numSpace) {
    let maxNumCol = Math.floor(CHRS/3);  // filename minimum 1 char + 2 spaces = 3
    let maxWidths = [[0]];
    let col = 0;
    let sum = 0;
    let widths = [];

    for (let j=0; j<filenames.length; j++) {
        widths.push(filenames[j].length+(filenames[j].includes(" ") ? 2+2 : numSpace+2));
    }

    //    numCol   [   0    ,    1    ,    2    , ...]
    //       0   =    [?]
    //       1   = [maxWidth]
    //       2   = [maxWidth, maxWidth]
    //       3   = [maxWidth, maxWidth, maxWidth]
    //       :   = [ ...
    // maxNumCol = [ ...
    maxNumCol = (filenames.length>maxNumCol ? maxNumCol : filenames.length);
    for (let i=1; i<=maxNumCol; i++) {  // for each column config
        maxWidths.push(new Array(i).fill(3));  // init config as an array of three(3)s
    }
    for (let i=1; i<=maxNumCol; i++) {  // for each column config
        for (let j=0; j<widths.length; j++) {
            col = Math.floor(j/(Math.ceil(widths.length/i)));
            if (widths[j]>maxWidths[i][col]) {  // if width > max width in that column
                maxWidths[i][col] = widths[j];  // then update max width in that column
            }
        }
    }
    for (let i=1; i<=maxNumCol; i++) {  // for each column config
        sum = 0;
        for (let j=0; j<i; j++) {
            sum = sum+maxWidths[i][j];  // sum all max widths
        }
        if (sum<=CHRS) {  // if sum <= terminal width
            maxWidths[0][0] = i;  // store the index of such column config
        }
    }

    return maxWidths[maxWidths[0][0]];  // return the largest possible column config
}

function listTabular(prettyFilenames, padCols) {
    let numPad = 0;
    let numRow = Math.ceil(prettyFilenames.length/padCols.length);
    let row = "";
    let index;  // calculated index of prettyFilenames[]

    for (let i=0; i<numRow; i++) {  // for each row
        row = "";
        for (let j=0; j<padCols.length; j++) {  // for each col
            index = i+numRow*j;  // pick the (i+numRow*j)'th file from pretty array for printing
            if (index<prettyFilenames.length) {
                numPad = padCols[j]-prettyFilenames[index].replaceAll(/\x1b\[.*?m/g, "").length;
                row = row+prettyFilenames[index]+" ".repeat(numPad);
            }
        }
        process.stdout.write(row.trimEnd()+"\n");
    }
}

DIRS.rs = "\x1b[0m";
let fileArgs = [];
let i = 0;
while (i<paths.length) {
    try {
        if (fs.statSync(paths[i]).isDirectory()) {
            i++;
        }
        else {
            fileArgs.push(paths.splice(i, 1)[0]);
        }
    }
    catch (error) {
        console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: cannot access '${paths[i]}':`));
        paths.splice(i, 1);
    }
}
paths.sort();
if (fileArgs.length>0) {
    paths.unshift("");
}

for (let [j, path] of paths.entries()) {
    let prettyFilenames = [];
    let filenames = (path=="" ? fileArgs : fs.readdirSync(path));
    let isAnySpace = (isSingle===undefined || !isSingle) && filenames.filter((filename) => filename.includes(" ")).length!=0;

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

    prettyFilenames = filenames.map(listPretty(isAnySpace, (path=="" ? "." : path)));  // the whole  ̲l̲i̲s̲t̲P̲r̲e̲t̲t̲y̲(̲i̲s̲A̲n̲y̲S̲p̲a̲c̲e̲,̲ ̲p̲a̲t̲h̲)̲ ̲ is a template function name
    if (paths.length>1 && path!="") {
        process.stdout.write(path+":\n");
    }
    if (isLong) {
        listLong(prettyFilenames);
    }
    else if (isSingle) {
        listSingle(prettyFilenames);
    }
    else {
        listTabular(prettyFilenames, calColConfig(filenames, (isAnySpace ? 1 : 0)));
    }
    if (j<paths.length-1) {
        process.stdout.write("\n");
    }
}