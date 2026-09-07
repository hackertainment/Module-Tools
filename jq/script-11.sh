#!/bin/bash

set -euo pipefail

# The input for this script is the scores.json file.
# TODO: Write a command to output the total of adding together all scores from all games from all players.
# Your output should be exactly the number 164.
cat scores.json |jq -r '[.[].scores |add] |add'