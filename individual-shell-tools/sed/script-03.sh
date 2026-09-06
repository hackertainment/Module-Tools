#!/bin/bash

set -euo pipefail

# TODO: Write a command to output input.txt removing any line which contains a number.
# The output should contain 6 lines.
sed '/^.*[0-9].*$/d' ./input.txt