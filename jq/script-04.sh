#!/bin/bash

set -euo pipefail

# The input for this script is the scores.json file.
# TODO: Write a command to output just the names of each player, one per line.
# Your output should contain 6 lines, each with just one word on it.
# Your output should not contain any quote characters.
cat scores.json |jq -r '.[].name'