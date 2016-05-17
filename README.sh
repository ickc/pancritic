#!/bin/bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Preparation: I made a copy first so that your README is not overwritten
cp README.md README-accept.md
cp README.md README-reject.md

# Some Examples
## Showing Difference and not overwriting
./pandoc-criticmarkup.sh -d html README.md | pandoc -s -c pandoc-criticmarkup.css -o README.html
./pandoc-criticmarkup.sh -d latex README.md | pandoc -s -o README.tex
./pandoc-criticmarkup.sh -d pdf README.md | pandoc -s -o README.pdf
## accept or reject while overwriting the source
### accept
./pandoc-criticmarkup.sh -ap README-accept.md
### reject
./pandoc-criticmarkup.sh -rp README-reject.md
## accept or reject, but keep the CriticMarkup in the source for future reference
### accept
./pandoc-criticmarkup.sh -a README.md | pandoc -s -c pandoc-criticmarkup.css -o README-accept.html
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.tex
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.pdf
### reject
./pandoc-criticmarkup.sh -r README.md | pandoc -s -c pandoc-criticmarkup.css -o README-reject.html
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.tex
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.pdf