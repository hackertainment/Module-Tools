#!/bin/bash

set -euo pipefail

# TODO: Write a command to output, for each `.txt` file in this directory, how many lines of dialogue the Doctor has.
# The output should show that dialogue.txt contains 6 lines, dialogue-2.txt contains 2, and dialogue-3.txt contains 0.
grep -c '^Doctor: ' ./*.txt