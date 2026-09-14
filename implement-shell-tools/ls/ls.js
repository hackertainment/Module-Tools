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

function listPretty(isPrependSpace, path) {
    return function (filename) {
        const [dir, ext] = process.env.LS_COLORS.replace(":*", "\n").split("\n");
        const dirs = Object.fromEntries(new URLSearchParams(dir.replaceAll("=", "=\x1b[").replaceAll(":", "m&")+"m"));
        const exts = Object.fromEntries(new URLSearchParams(ext.replaceAll("=", "=\x1b[").replaceAll(":", "m&")));
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

        if (lstats.isDirectory() && (lstats.mode&0o1000)!=0 && (lstats.mode&0o0002)!=0) {
            filename = dirs.tw+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isDirectory() && (lstats.mode&0o0002)!=0) {
            filename = dirs.ow+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isDirectory() && (lstats.mode&0o1000)!=0) {
            filename = dirs.st+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isDirectory()) {
            filename = dirs.di+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isSymbolicLink() && isExist) {
            filename = dirs.ln+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isSymbolicLink() && !isExist) {
            filename = dirs.or+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.nlink>1) {
            filename = dirs.mh+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isFIFO()) {
            filename = dirs.pi+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isSocket()) {
            filename = dirs.so+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isBlockDevice()) {
            filename = dirs.bd+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isCharacterDevice()) {
            filename = dirs.cd+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isFile() && (lstats.mode&0o4000)!=0) {
            filename = dirs.su+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isFile() && (lstats.mode&0o2000)!=0) {
            filename = dirs.sg+prefix+filename+suffix+dirs.rs;
        }
        else if (lstats.isFile() && (lstats.mode&0o0111)!=0) {
            filename = dirs.ex+prefix+filename+suffix+dirs.rs;
        }
        else if (Object.keys(exts).includes("*."+filename.split(".").pop())) {
            filename = exts["*."+filename.split(".").pop()]+prefix+filename+suffix+dirs.rs;
        }
        else {
            filename = prefix+filename+suffix;
        }

        return filename;
    }
}

function listTabular(filenames) {
    for (let filename of filenames) {
        process.stdout.write(filename+"  ");
    }
    process.stdout.write("\n");
}

for (let [i, path] of paths.entries()) {
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

    if (paths.length>1) {
        process.stdout.write(path+":\n");
    }
    listTabular(filenames.map(listPretty(isAnySpace, path)));  // the whole  ̲l̲i̲s̲t̲P̲r̲e̲t̲t̲y̲(̲i̲s̲A̲n̲y̲S̲p̲a̲c̲e̲,̲ ̲p̲a̲t̲h̲)̲ ̲ is a template function name
    if (i<paths.length-1) {
        process.stdout.write("\n");
    }
}