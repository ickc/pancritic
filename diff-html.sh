#!/bin/bash

# get paths and extension
PATHNAME="$@"
PATHNAMEWOEXT=${PATHNAME%.*}
EXT=${PATHNAME##*.}
# ext="${EXT,,}" #This does not work on Mac's default, old version of, bash.

# copy
cp "$@" "$PATHNAMEWOEXT-diff-html.$EXT"

# replace
## sub
sed -i '' s/'~~}'/'<\/ins>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'{~~'/'<del>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'~>'/'<\/del><ins>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
## del
sed -i '' s/'{--'/'<del>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'--}'/'<\/del>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
## ins
sed -i '' s/'{++'/'<ins>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'++}'/'<\/ins>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
## mark
sed -i '' s/'{=='/'<mark>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'==}'/'<\/mark>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
## comment
sed -i '' s/'{>>'/'<aside>'/g "$PATHNAMEWOEXT-diff-html.$EXT"
sed -i '' s/'<<}'/'<\/aside>'/g "$PATHNAMEWOEXT-diff-html.$EXT"