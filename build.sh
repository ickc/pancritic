#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

./pandoc-criticmarkup.sh -d html README.md | pandoc -s -o README-diff.html
./pandoc-criticmarkup.sh -d latex README.md | pandoc -s -o README-diff.tex
./pandoc-criticmarkup.sh -d pdf README.md | pandoc -s -o README-diff.pdf

./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.html
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.tex
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.pdf

./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.html
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.tex
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.pdf