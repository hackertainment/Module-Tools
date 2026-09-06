#!/bin/bash

set -euo pipefail

# TODO: Write a command to output input.txt with one fix:
# If a comma in input.txt is not followed by a space, add a space after.
# If there is already a space after a comma, do not add an additional space.
# The output should contain 11 lines.
# Line 3 should be "It contains many lines, and there are some things you may want to do with each of them.".
# Line 11 should be "We also should remember, when we go shopping, to get 4 items: oranges, cheese, bread, olives.".
sed 's/,\([^ ]\)/, \1/g' ./input.txt