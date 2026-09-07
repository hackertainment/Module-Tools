#!/bin/bash

set -euo pipefail

# The input for this script is the scores.json file.
# TODO: Write a command to output just the names of each player along with the score from their first attempt.
# Your output should contain 6 lines, each with one word and one number on it.
# The first line should be "Ahmed 1" with no quotes.
cat scores.json |jq -r '.[] |[.name,.scores.[0]] |join(" ")'