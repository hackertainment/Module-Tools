#!/bin/bash

set -euo pipefail

# The input for this script is the text.txt file, which contains an email.
# The author got feedback that they're using too many exclamation marks (!).
#
# TODO: Write a command to output the contents of text.txt with every exclamation mark (!) replaced with a full-stop (.).
tr '!' '.' <text.txt