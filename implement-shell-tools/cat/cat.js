#!/home/ec2-user/.nvm/versions/node/v24.19.0/bin/node

import { program } from "commander";
import { promises as fs } from "node:fs";
import process from "node:process";

const TOOL_NAME = process.argv[1].split("/").pop();
const TOOL_AUTHOR = "Wyatt L.";

program
    .name(TOOL_NAME)
    .usage("[OPTION]... [FILE]...")
    .description("Concatenate FILE(s) to standard output.\n\nWith no FILE, or when FILE is -, read standard input.")
    .option("-b, --number-nonblank", "number nonempty output lines, overrides -n")
    .option("-n, --number", "number all output lines")
    .helpOption("--help", "display this help and exit")
    .version(`${TOOL_NAME} (CYF shelltools) 1.00\n\nWritten by ${TOOL_AUTHOR}`, "--version", "output version information and exit")
    .addHelpText("after", `\nExamples:\n  ${TOOL_NAME} f - g  Output f's contents, then standard input, then g's contents.\n  ${TOOL_NAME}        Copy standard input to standard output.`)
    .argument("[FILE...]", null, ["-"]);

program.parse();

const files = program.args;
const isNumber = program.opts().number;
const isNonblank = program.opts().numberNonblank;

// commander cannot specify a default value for an optional command-argument
if (files.length==0) {
    files.push("-");
}

for (let file of files) {
    try {
        let content = await fs.readFile(file, "utf-8");
        let lines = content.split("\n");
        let i = 0;

        while (i<lines.length-1) {
            if (isNumber) {
                process.stdout.write((i+1).toString().padStart(6, " ")+"  ");
            }
            process.stdout.write(lines[i]+"\n");
            i++;
        }

        // handle special case whether with or without trailing \n
        if (isNumber && lines[i]!="") {
            process.stdout.write((i+1).toString().padStart(6, " ")+"  ");
        }
        process.stdout.write(lines[i]);
    }
    catch (error) {
        console.error(error.message.split(",")[0].replace(/^[A-Z]*:/, `${TOOL_NAME}: ${file}:`));
    }
}