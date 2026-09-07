#!/bin/bash

set -euo pipefail

# The input for this script is the scores-table.txt file.
# TODO: Write a command to output scores-table.txt, with shows the lines for the three players with the highest first score, in descending order.
# Your output should be:
# Basia London 22 9 6
# Piotr Glasgow 15 2 25 11 8
# Chandra Birmingham 12 6
sort -nrk3 ./scores-table.txt |head -n3