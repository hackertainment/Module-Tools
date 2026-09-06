#!/bin/bash

set -euo pipefail

# TODO: Write a command to output input.txt with all occurrences of the letter `i` replaced with `I`.
# The output should contain 11 lines.
# The first line of the output should be: "ThIs Is a sample fIle for experImentIng wIth sed.".
sed 's/i/I/g' ./input.txt