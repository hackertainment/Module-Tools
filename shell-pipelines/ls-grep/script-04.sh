#!/bin/bash

set -euo pipefail

# TODO: Write a command to count the number of files in the sample-files directory whose name starts with an upper case letter and doesn't contain any other upper case letters.
# Your output should be the number 7.
ls ./sample-files/ |grep -c '^[A-Z][a-z]*$'