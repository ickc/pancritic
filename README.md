---
title: Using CriticMarkup with pandoc
author: Kolen Cheung
usepackage: [color,soul]
---

Using CriticMarkup with pandoc---not a filter but a preprocessor.

# Definition of CriticMarkup #

- Deletions: This is {--is --}a test.
- Additions: This {++is ++}a test.
- Substitutions: This {~~isn't~>is~~} a test.
- Highlighting: This is a {==test==}.
- Comments: This is a test{>>What is a test for?<<}.

# The Scripts #

These scripts are supposed to be in the same folder:

- `criticmarkup-accept.py`- `criticmarkup-reject.py`- `pandoc-criticmarkup.sh`

The `criticmarkup-accept.py` and `criticmarkup-reject.py` are extracted from the OS X System Services from [CriticMarkup Toolkit](http://criticmarkup.com/services.php).

Note that the latex output requires the LaTeX packages `color` and `soul`. As you can see from this markdown file, I have an YAML of `usepackage: [color,soul]`, that in my template will added `\usepackage{color,soul}`. See [ickc/pandoc-templates at latex-usepackage-hyperref](https://github.com/ickc/pandoc-templates/tree/latex-usepackage-hyperref).

# Usage #

`pandoc-criticmarkup.sh [options...] [file]`

Options:

- accept: `-a`
- reject: `-r`
- permanent: `-p`
- show diff: `-d`
	- `-d html`: targeting html output using RAW HTML
	- `-d latex`: targeting LaTeX output using RAW LaTeX
	- `-d pdf`: same as above

If permanent is used, it will overwrite the original, if not, it will output to `stdout`. In most situation permanent should be used with `-a` or `-r` only, but it can be used with `-d` as well.

`-a`, `-r`, `-d` are supposed to use separately:

- If `-d` is used, the others are ignored,
- if `-r` is used, `-a` is ignored

It can be used with the pandoc commands, like these (see build.sh):

```bash
./pandoc-criticmarkup.sh -d html README.md | pandoc -s -o README-diff.html
./pandoc-criticmarkup.sh -d latex README.md | pandoc -s -o README-diff.tex
./pandoc-criticmarkup.sh -d pdf README.md | pandoc -s -o README-diff.pdf

./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.html
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.tex
./pandoc-criticmarkup.sh -a README.md | pandoc -s -o README-accept.pdf

./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.html
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.tex
./pandoc-criticmarkup.sh -r README.md | pandoc -s -o README-reject.pdf  
```

# Appendix: Mapping for Showing Differences #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `{--[text]--}`	| `<del>[text]</del>`	| `\st{[text]}`	|  
| `{++[text]++}`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `{~~[text1]~>[text2]~~}`	| `<del>[text1]</del><ins>[text2]</ins>`	| `\st{[text1]}\underline{[text2]}`	| 
| `{==[text]==}`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `{>>[text]<<}`	| `<aside>[text]</aside>`	| `\marginpar{[text]}`	|  