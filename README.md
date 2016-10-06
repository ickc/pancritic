---
title: Using CriticMarkup with pandoc
author: Kolen Cheung
fontfamily: lmodern,color,soul
...

Using CriticMarkup with pandoc---not a filter but a preprocessor.

# Definition of CriticMarkup #

- Deletions: This is {--is --}a test.
- Additions: This {++is ++}a test.
- Substitutions: This {~~isn't~>is~~} a test.
- Highlighting: This is a {==test==}.
- Comments: This is a test{>>What is a test for?<<}.

# The Scripts #

- `pandoc-criticmarkup.sh`
	- `criticmarkup-reject.py`
	- `criticmarkup-accept.py`

`pandoc-criticmarkup.sh` will looks for the other 2 scripts in the same folder.

The `criticmarkup-accept.py` and `criticmarkup-reject.py` are extracted from the OS X System Services from [CriticMarkup Toolkit](http://criticmarkup.com/services.php).

## Note on LaTeX Output: Usepackage Required ##

Note that the LaTeX output requires the LaTeX packages `color` and `soul`.

One can achieve this by either using a custom template or `--include-in-header` option. Or you can use the trick of putting the following in your YAML front matter, like this file:

```yaml
---
fontfamily: lmodern,color,soul
...
```

# Usage #

`pandoc-criticmarkup.sh [options...] [file]`

Options:

- if no filename is given, it reads from the stdin
- accept: `-a`
- reject: `-r`
- permanent: `-p`
- show diff: `-d`
	- `-d html`: targeting html output using raw HTML
	- `-d tex`: targeting LaTeX output using raw LaTeX
	- `-d pdf`: same as above

If permanent is used, it will overwrite the original, if not, it will output to `stdout`. In most situation permanent should be used with `-a` or `-r` only, but it can be used with `-d` as well.

`-a`, `-r`, `-d` are supposed to use separately:

- If `-d` is used, the others are ignored,
- if `-r` is used, `-a` is ignored

It can be used with the pandoc commands, like these:

```bash
## Showing Difference and not overwriting
./pandoc-criticmarkup.sh -d html README.md | pandoc -s -o README.html
./pandoc-criticmarkup.sh -d pdf README.md | pandoc -s -o README.pdf
## accept or reject while overwriting the source
./pandoc-criticmarkup.sh -ap README-accept.md
./pandoc-criticmarkup.sh -rp README-reject.md
```

# Caveats

The way this script works depends on the fact that pandoc allows raw HTML and raw LaTeX in the markdown source. The CriticMarkup is transformed into either a raw HTML or raw LaTeX representation (specified by the command line arguments).

Because of the asymmetry in the way pandoc handle raw HTML and raw LaTeX (namely, markdown inside raw HTML are parsed, but not in raw LaTeX), markdown within the CriticMarkup will not be rendered in LaTeX output. If you want to change this behavior, you can take a look at: [LaTeX Argument Parser](https://gist.github.com/mpickering/f1718fcdc4c56273ed52).

Another caveat is that nesting CriticMarkup might have unexpected behavior, especially in LaTeX output. For example, the [test.md](test.md) file do not have a valid LaTeX output because of nesting CriticMarkup.

Lastly, see [the caveats section in the spec of CriticMarkup](http://criticmarkup.com/spec.php#caveats).

# Todo #

- add a minimal CSS (especially for the HTML aside element)

# Appendix

## CSS ##

An optional CSS `pandoc-criticmarkup.css` make the deletions and additions more obvious in HTML output.

## Mapping for Showing Differences ##

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `{--[text]--}`	| `<del>[text]</del>`	| `\st{[text]}`	|  
| `{++[text]++}`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `{~~[text1]~>[text2]~~}`	| `<del>[text1]</del><ins>[text2]</ins>`	| `\st{[text1]}\underline{[text2]}`	| 
| `{==[text]==}`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `{>>[text]<<}`	| `<aside>[text]</aside>`	| `\marginpar{[text]}`	|  

## Test Files From MMD ##

[test.md](test.md) is from [MMD-Test-Suite/Critic.text at master · fletcher/MMD-Test-Suite](https://github.com/fletcher/MMD-Test-Suite/blob/master/CriticMarkup/Critic.text)