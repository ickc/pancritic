#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

./diff-html.sh ./README.md
./diff-latex.sh ./README.md
pandoc -s -o test-diff-html.html README-diff-html.md
pandoc -s -o test-diff-latex.tex README-diff-latex.md
pandoc -s -o test-diff-latex.pdf README-diff-latex.md