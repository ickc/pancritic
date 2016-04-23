#!/bin/bash

# get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
# ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.

# copy
cp "$@" "$PATHNAMEWOEXT-diff-latex.$EXT"

# replace
## sub
sed -i '' s/'~~}'/'}'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'{~~'/'\\st{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'~>'/'}\\underline{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
## del
sed -i '' s/'{--'/'\\st{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'--}'/'}'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
## ins
sed -i '' s/'{++'/'\\underline{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'++}'/'}'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
## mark
sed -i '' s/'{=='/'\\hl{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'==}'/'}'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
## comment
sed -i '' s/'{>>'/'\\marginpar{'/g "$PATHNAMEWOEXT-diff-latex.$EXT"
sed -i '' s/'<<}'/'}'/g "$PATHNAMEWOEXT-diff-latex.$EXT"