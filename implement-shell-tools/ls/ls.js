#!/home/ec2-user/.nvm/versions/node/v24.19.0/bin/node

import { program } from "commander";
import { promises as fs } from "node:fs";
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
    .version(`${TOOL_NAME} (CYF shelltools) 1.00\n\nWritten by ${TOOL_AUTHOR}`, "--version", "output version information and exit")
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

function listPretty(isPrependSpace) {
    return function (filename) {
        const [dir, ext] = process.env.LS_COLORS.replace(":*", "\n").split("\n");
        const dirs = Object.fromEntries(new URLSearchParams(dir.replaceAll("=", "=\x1b[").replaceAll(":", "m&")+"m"));
        const exts = Object.fromEntries(new URLSearchParams(ext.replaceAll("*", "").replaceAll("=", "=\x1b[").replaceAll(":", "m&")));
    
        // if filename has space, add single quote to it and leading space to others
        if (filename.includes(" ")) {
            filename = "'"+filename+"'";
        }
        else if (isPrependSpace) {
            filename = " "+filename;
        }

        return filename;
    }
}

function listTabular(filenames) {
    console.table(filenames);
}

for (let [i, path] of paths.entries()) {
    let filenames = await fs.readdir(path);
    let isAnySpace = filenames.filter((filename) => filename.includes(" ")).length!=0;

    if (paths.length>1) {
        process.stdout.write(path+":\n");
    }
    listTabular(filenames.sort().map(listPretty(isAnySpace)));  // the whole _listPretty(isAnySpace)_ is a template function
    if (i<paths.length-1) {
        process.stdout.write("\n");
    }
}