#!/bin/bash

set -euo pipefail

# Do not change this part of the script - only change after the TODO comment.

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
if [[ "${script_dir}" != "$(pwd)" ]]; then
  echo >&2 "ERROR: You haven't cd'd into the correct directory."
  echo >&2 "For each exercise, you should cd to the directory containing the script before running it."
  exit 1
fi

# TODO: Write a command to list the files and folders in this directory.
# The output should be a list of names including child-directory, script-01.sh, script-02.sh, and more.
ls ./