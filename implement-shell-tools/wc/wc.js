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
    .option("-c, --bytes", "print the byte counts")
    .option("-l, --lines", "print the newline counts")
    .option("-m, --chars", "print the character counts")
    .option("-w, --words", "print the word counts")
    .helpOption("--help", "display this help and exit")
    .version(TOOL_VERSION, "--version", "output version information and exit")
    .addHelpText("after", TOOL_CAVEAT)
    .argument("[FILE...]", null, ["-"])
    .parse();

const files = program.args;
const isByte = (Object.keys(program.opts()).length==0 ? true : (program.opts().bytes===undefined ? false : program.opts().bytes));
const isChar = (Object.keys(program.opts()).length==0 ? false : (program.opts().chars===undefined ? false : program.opts().chars));
const isLine = (Object.keys(program.opts()).length==0 ? true : (program.opts().lines===undefined ? false : program.opts().lines));
const isWord = (Object.keys(program.opts()).length==0 ? true : (program.opts().words===undefined ? false : program.opts().words));

// commander not correctly specify default value for an optional command-argument
if (files.length==0) {
    files.push("");
}

let counts = {line:0, word:0, char:0, byte:0};
let totals = {line:0, word:0, char:0, byte:0};
let padSize = 7;  // default padding size when any file is stdin
let content = "";

// https://dmitripavlutin.com/what-every-javascript-developer-should-know-about-unicode/
async function count(filename) {
    try {
        content = await fs.readFile(filename, "utf-8");
        counts.line = (content.match(/\n/g)==null ? 0 : content.match(/\n/g).length);
        counts.word = (content.match(/\S+/g)==null ? 0 : content.match(/\S+/g).length);
        counts.char = [...content].length;
        counts.byte = Buffer.byteLength(content);
    }
    catch (error) {
        throw error;
    }
}

// prepare padding size when no file is stdin
if (!files.includes("-") && !files.includes("")) {
    for (let file of files) {
        try {
            await count(file);
            Object.keys(totals).forEach(key => {totals[key] += counts[key]});  // totals.____ += counts.____
        }
        catch {
            //console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: ${file}:`));
        }
    }
    padSize = 0;
    if (isLine && totals.line.toString().length>padSize) {
        padSize = totals.line.toString().length;
    }
    if (isWord && totals.word.toString().length>padSize) {
        padSize = totals.word.toString().length;
    }
    if (isChar && totals.char.toString().length>padSize) {
        padSize = totals.char.toString().length;
    }
    if (isByte && totals.byte.toString().length>padSize) {
        padSize = totals.byte.toString().length;
    }
    Object.keys(totals).forEach(key => {totals[key] = 0});  // totals.____ = 0
}

// count and print each file including stdin
for (let file of files) {
    try {
        await count((file=="-" || file=="") ? "/dev/stdin" : file);
        Object.keys(totals).forEach(key => {totals[key] += counts[key]});  // totals.____ += counts.____
        if (isLine) {
            process.stdout.write(counts.line.toString().padStart(padSize, " ")+ " ");
        }
        if (isWord) {
            process.stdout.write(counts.word.toString().padStart(padSize, " ")+ " ");
        }
        if (isChar) {
            process.stdout.write(counts.char.toString().padStart(padSize, " ")+ " ");
        }
        if (isByte) {
            process.stdout.write(counts.byte.toString().padStart(padSize, " ")+ " ");
        }
        process.stdout.write(file+"\n");
    }
    catch (error) {
        console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: ${file}:`));
    }
}
if (files.length>1) {
    if (isLine) {
        process.stdout.write(totals.line.toString().padStart(padSize, " ")+ " ");
    }
    if (isWord) {
        process.stdout.write(totals.word.toString().padStart(padSize, " ")+ " ");
    }
    if (isChar) {
        process.stdout.write(totals.char.toString().padStart(padSize, " ")+ " ");
    }
    if (isByte) {
        process.stdout.write(totals.byte.toString().padStart(padSize, " ")+ " ");
    }
    process.stdout.write("total\n");
}