#!/home/ec2-user/.nvm/versions/node/v24.19.0/bin/node

import { program } from "commander";
import { promises as fs } from "node:fs";
import process from "node:process";

const TOOL_NAME = process.argv[1].split("/").pop();
const TOOL_AUTHOR = "Wyatt L.";
const TOOL_VERSION = `${TOOL_NAME} (CYF shelltools) 1.00\n\nWritten by ${TOOL_AUTHOR}`;
const TOOL_CAVEAT = `
Examples:
  ${TOOL_NAME} f - g  Output f's contents, then standard input, then g's contents.
  ${TOOL_NAME}        Copy standard input to standard output.
`;

program
    .name(TOOL_NAME)
    .usage("[OPTION]... [FILE]...")
    .description("Concatenate FILE(s) to standard output.\n\nWith no FILE, or when FILE is -, read standard input.")
    .option("-b, --number-nonblank", "number nonempty output lines, overrides -n")
    .option("-n, --number", "number all output lines")
    .helpOption("--help", "display this help and exit")
    .version(TOOL_VERSION, "--version", "output version information and exit")
    .addHelpText("after", TOOL_CAVEAT)
    .argument("[FILE...]", null, ["-"])
    .parse();

const files = program.args;
const isNonblank = program.opts().numberNonblank;
const isNumber = (isNonblank ? false : program.opts().number);

// commander not correctly specify default value for an optional command-argument
if (files.length==0) {
    files.push("-");
}

let isNewline = true;
let count = 0;

for (let file of files) {
    try {
        let content = await fs.readFile((file=="-" ? "/dev/stdin" : file), "utf-8");  // TODO: should echo line immediately when pressing enter
        let lines = content.split("\n");
        let i = 0;

        while (i<lines.length-1) {
            if ((isNumber || (isNonblank && lines[i]!="")) && isNewline) {
                process.stdout.write((++count).toString().padStart(6, " ")+"  ");
            }
            process.stdout.write(lines[i]+"\n");
            isNewline = true;
            i++;
        }

        // handle special case when file without trailing \n
        //if ((isNumber || (isNonblank && lines[i]!="")) && lines[i]!="" && isNewline) {
        if ((isNumber || isNonblank) && lines[i]!="" && isNewline) {
            process.stdout.write((++count).toString().padStart(6, " ")+"  ");
            isNewline = false;
        }
        process.stdout.write(lines[i]);
    }
    catch (error) {
        console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: ${file}:`));
    }
}