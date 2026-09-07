#!/bin/bash

set -euo pipefail

# The input for this script is the scores-table.txt file.
# TODO: Write a command to output scores-table.txt, with lines sorted by the person's first score, descending.
# The first line of your output should be "Basia London 22 9 6" (with no quotes).
sort -nrk3 ./scores-table.txt