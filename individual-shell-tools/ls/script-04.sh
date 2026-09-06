#!/bin/bash

set -euo pipefail

# Do not change this part of the script - only change after the TODO comment.

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
touch "${script_dir}/child-directory/helper-2.txt"
sleep 1
touch "${script_dir}/child-directory/helper-1.txt"
sleep 1
touch "${script_dir}/child-directory/helper-3.txt"

echo "First exercise (sorted newest to oldest):"

# TODO: Write a command which lists the files in the child-directory directory, one per line, sorted so that the most recently modified file is first.
# The output should be a list of names in this order, one per line: helper-3.txt, helper-1.txt, helper-2.txt.
ls -lt ./child-directory/

echo "Second exercise (sorted oldest to newest):"

# TODO: Write a command which does the same as above, but sorted in the opposite order (oldest first).
# The output should be a list of names in this order, one per line: helper-2.txt, helper-1.txt, helper-3.txt.
ls -ltr ./child-directory/