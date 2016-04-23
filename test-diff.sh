#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

./diff-html.sh ./test.md
./diff-latex.sh ./test.md
pandoc -s -o test-diff-html.html test-diff-html.md
pandoc -s -o test-diff-latex.pdf test-diff-latex.md