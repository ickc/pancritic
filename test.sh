#!/bin/bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# test/test folder
mkdir -p test

# README.md

## Preparation: I made a copy first so that your README is not overwritten
cp README.md test/README-accept.md
cp README.md test/README-reject.md

## Some Examples
### Showing Difference and not overwriting
pandoc-criticmarkup.sh -d html README.md | pandoc -s -c pandoc-criticmarkup.css -o test/README.html
pandoc-criticmarkup.sh -d latex README.md | pandoc -s -o test/README.tex
pandoc-criticmarkup.sh -d pdf README.md | pandoc -s -o test/README.pdf
### accept or reject while overwriting the source
#### accept
pandoc-criticmarkup.sh -ap test/README-accept.md
#### reject
pandoc-criticmarkup.sh -rp test/README-reject.md
## accept or reject, but keep the CriticMarkup in the source for future reference
#### accept
pandoc-criticmarkup.sh -a README.md | pandoc -s -c pandoc-criticmarkup.css -o test/README-accept.html
pandoc-criticmarkup.sh -a README.md | pandoc -s -o test/README-accept.tex
pandoc-criticmarkup.sh -a README.md | pandoc -s -o test/README-accept.pdf
#### reject
pandoc-criticmarkup.sh -r README.md | pandoc -s -c pandoc-criticmarkup.css -o test/README-reject.html
pandoc-criticmarkup.sh -r README.md | pandoc -s -o test/README-reject.tex
pandoc-criticmarkup.sh -r README.md | pandoc -s -o test/README-reject.pdf

# test.md

## Preparation: I made a copy first so that your test is not overwritten
cp test.md test/test-accept.md
cp test.md test/test-reject.md

## Some Examples
### Showing Difference and not overwriting
pandoc-criticmarkup.sh -d html test.md | pandoc -s -c pandoc-criticmarkup.css -o test/test.html
pandoc-criticmarkup.sh -d latex test.md | pandoc -s -o test/test.tex
pandoc-criticmarkup.sh -d pdf test.md | pandoc -s -o test/test.pdf
### accept or reject while overwriting the source
### accept
pandoc-criticmarkup.sh -ap test/test-accept.md
#### reject
pandoc-criticmarkup.sh -rp test/test-reject.md
## accept or reject, but keep the CriticMarkup in the source for future reference
#### accept
pandoc-criticmarkup.sh -a test.md | pandoc -s -c pandoc-criticmarkup.css -o test/test-accept.html
pandoc-criticmarkup.sh -a test.md | pandoc -s -o test/test-accept.tex
pandoc-criticmarkup.sh -a test.md | pandoc -s -o test/test-accept.pdf
#### reject
pandoc-criticmarkup.sh -r test.md | pandoc -s -c pandoc-criticmarkup.css -o test/test-reject.html
pandoc-criticmarkup.sh -r test.md | pandoc -s -o test/test-reject.tex
pandoc-criticmarkup.sh -r test.md | pandoc -s -o test/test-reject.pdf
