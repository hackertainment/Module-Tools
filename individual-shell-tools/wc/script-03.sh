#!/bin/bash

set -euo pipefail

# TODO: Write a command to output the number of lines, words, and characters in all of the files inside the helper-files directory.
# The output should be something like:
#        1       4      20 ../helper-files/helper-1.txt
#        1       7      39 ../helper-files/helper-2.txt
#        3      19      92 ../helper-files/helper-3.txt
#        5      30     151 total
wc ../helper-files/*