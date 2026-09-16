#!/home/ec2-user/.nvm/versions/node/v24.19.0/bin/node

import { program } from "commander";
import { promises as fs } from "node:fs";
import process from "node:process";

const TOOL_NAME = process.argv[1].split("/").pop();
const TOOL_AUTHOR = "Wyatt L.";
const TOOL_VERSION = `${TOOL_NAME} (CYF shelltools) 1.00\n\nWritten by ${TOOL_AUTHOR}`;
const TOOL_CAVEAT = ``;

program
    .name(TOOL_NAME)
    .usage("[OPTION]... [FILE]...\n  or:  "+TOOL_NAME+" [OPTION]... --files0-from=F")
    .description("Print newline, word, and byte counts for each FILE, and a total line if\nmore than one FILE is specified.  A word is a non-zero-length sequence of\ncharacters delimited by white space.\n\nWith no FILE, or when FILE is -, read standard input.\n\nThe options below may be used to select which counts are printed, always in\nthe following order: newline, word, character, byte, maximum line length.")
    .option("-c, --bytes", "print the byte counts", true)
    .option("-l, --lines", "print the newline counts", true)
    .option("-w, --words", "print the word counts", true)
    .helpOption("--help", "display this help and exit")
    .version(TOOL_VERSION, "--version", "output version information and exit")
    .addHelpText("after", TOOL_CAVEAT)
    .argument("[FILE...]", null, ["-"])
    .parse();

const files = program.args;
const isByte = program.opts().bytes;
const isLine = program.opts().lines;
const isWord = program.opts().words;

// commander not correctly specify default value for an optional command-argument
if (files.length==0) {
    files.push("-");
}

for (let file of files) {
    try {
        let content = await fs.readFile((file=="-" ? "/dev/stdin" : file), "utf-8");  // TODO: should echo line immediately when pressing enter
        //console.log(content);
    }
    catch (error) {
        console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: ${file}:`));
    }
}