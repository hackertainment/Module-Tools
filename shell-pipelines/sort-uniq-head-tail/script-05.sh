#!/bin/bash

set -euo pipefail

# The input for this script is the events.txt file.
# TODO: Write a command to show a list of all events that have happened, without duplication.
# The order they're displayed doesn't matter, but we never want to see the same event listed twice.
# Your output should contain 6 lines.
sort events.txt |uniq