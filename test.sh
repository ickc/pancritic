#!/bin/bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Preparation: I made a copy first so that your test is not overwritten
cp test.md test-accept.md
cp test.md test-reject.md

# Some Examples
## Showing Difference and not overwriting
./pandoc-criticmarkup.sh -d html test.md | pandoc -s -c pandoc-criticmarkup.css -o test.html
./pandoc-criticmarkup.sh -d latex test.md | pandoc -s -o test.tex
./pandoc-criticmarkup.sh -d pdf test.md | pandoc -s -o test.pdf
## accept or reject while overwriting the source
### accept
./pandoc-criticmarkup.sh -ap test-accept.md
### reject
./pandoc-criticmarkup.sh -rp test-reject.md
## accept or reject, but keep the CriticMarkup in the source for future reference
### accept
./pandoc-criticmarkup.sh -a test.md | pandoc -s -c pandoc-criticmarkup.css -o test-accept.html
./pandoc-criticmarkup.sh -a test.md | pandoc -s -o test-accept.tex
./pandoc-criticmarkup.sh -a test.md | pandoc -s -o test-accept.pdf
### reject
./pandoc-criticmarkup.sh -r test.md | pandoc -s -c pandoc-criticmarkup.css -o test-reject.html
./pandoc-criticmarkup.sh -r test.md | pandoc -s -o test-reject.tex
./pandoc-criticmarkup.sh -r test.md | pandoc -s -o test-reject.pdf