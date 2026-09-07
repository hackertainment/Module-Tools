#!/bin/bash

set -euo pipefail

# TODO: Write a command to output the names of the files in the sample-files directory whose name starts with an upper case letter and doesn't contain any other upper case letters.
# Your output should contain 7 files.
ls ./sample-files/ |grep '^[A-Z][a-z]*$'