#!/bin/bash

set -euo pipefail

# The input for this script is the text.txt file, which contains an email.
# Unfortunately, the author wrote it using a German keyboard which has the Y and Z keys swapped,
# so every Y should be a Z, and every Z should be a Y!
#
# TODO: Write a command to output the contents of text.txt with every Y and Z swapped (both upper and lower case).
cat text.txt |tr 'Yy' '<>' |tr 'Zz' 'Yy' |tr '<>' 'Zz'