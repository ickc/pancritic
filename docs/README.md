---
title: Using CriticMarkup with pandoc
author: Kolen Cheung
fontfamily: lmodern,changes
...

Using CriticMarkup with pandoc. It serves both as a wrapper and a pre-processor.

# Definition of CriticMarkup

- Deletions: This is \{\-\-is \-\-\}a test.
- Additions: This \{++is ++\}a test.
- Substitutions: This \{\~\~isn't\~\>is\~\~\} a test.
- Highlighting: This is a \{==test==\}.
- Comments: This is a test\{\>\>What is a test for?\<\<\}.

# Installation

Install using

```bash
pip install pancritic
```

# Usage: pancritic as a markdown wrapper (including but not limited to pandoc)

pancritic provides a pandoc-like cli. Pandoc users will feel right at home. See help from

```bash
pancritic -h
```

A typical use of pancritic will be like

```bash
pancritic -s -o index.html index.md
```

See examples in [HTML](tests.html) and [PDF](tests.pdf).

## pancritic specific options

`--engine`

: The default engine is `markdown`. Valid options are `markdown`, `markdown2`, `panflute`, `pypandoc`. You need to install the respective package in order to use them. `markdown` and `markdown2` are pure Python, hence useful for other CPU architechture. `panflute` and `pypandoc` both uses pandoc as backend.

`-m`|`--critic-mode`

: a/accept, r/reject: accept/reject changes.
: d/diff: generates a diff. In HTML output, JS is used for toggling between diff, accept, reject.
: m/markup: treat the CriticMarkup as Markup. i.e. in HTML output there isn't any toggles but the diff view only. In LaTeX output, diff and markup modes are identical except for an additional nav. `-m m` should be used with LaTeX output.

## Previous Users

### Previous Users of pandoc-criticmarkup

This is completely rewritten in Python. The cli has been completely changed too. The former options of `-a`, `-r`, `-d` are replaced with `-m a`, `-m r`, `-m d`, and added a `-m m`.

### Previous Users of `criticParser_CLI.py`

This is a heavy fork of `criticParser_CLI.py`, with these differences:

1. CLI has changed, with a more pandoc-like interface.
2. Python 3 (and 2) compatible.
3. Bug fixes (formerly hightlight without comment are parsed incorrectly).
4. It has much more input/output format options as well as engines.

Examples,

```bash
criticParser_CLI.py input.md -m2 -o output.html --css css.html
# is equivalent to
pancritic -o output.html input.md --critic-template css.html --engine markdown2
```

## Advanced Usage: pancritic as a pandoc preprocessor

A somewhat surprising behavior is when the to-format and output extension is different. In pancritic, the to-format indicates the CriticMarkup parsing behavior (mainly tex vs. html). And the output extension controls the final output's format (e.g. markdown, html, etc.)

An interesting use of this is to use pancritic as a pandoc preprocessor instead, like this

```bash
pancritic input.md -t markdown -m m | pandoc -s -o output.html
```

This will be useful if more advanced pandoc args are needed.

# Caveats

- Nesting CriticMarkup might have unexpected behavior, especially in LaTeX output. See [the caveats section in the spec of CriticMarkup](http://criticmarkup.com/spec.php#caveats).

- mainly tested with HTML and LaTeX output. RST output almost works, but injecting CSS/JS into the output causes some problems. Currently, it can be get arround with `--critic-template` and injecting the CSS/JS manually. See `pancritic/template.py` for the template used.

## LaTeX Ouptut

Note that the LaTeX output requires the LaTeX packages `changes>=3`.[^changes]

[^changes]: The version of the package in TeXLive 2018 is still v2. [TeXLive 2019 should be available on 2019-4-30](https://www.tug.org/texlive/), meanwhile you need to

	```bash
	# sudo is needed in most cases, depending on where you put it
	sudo tlmgr update --self
	sudo tlmgr update changes
	# check it is >=3
	tlmgr info changes
	```

One can tell pandoc to use this package by either using a custom template or `--include-in-header` option. Or you can use the trick of putting the following in your YAML front matter, like this file:

``` yaml
---
fontfamily: lmodern,changes
...
```

Markdown within the CriticMarkup will not be rendered in LaTeX output. If you want to change this behavior, you can take a look at: [LaTeX Argument Parser](https://gist.github.com/mpickering/f1718fcdc4c56273ed52).

| CriticMarkup	| LaTeX	|  
| ------------------------------------------	| ----------------------------------------------	|  
| `{--[text]--}`	| `\deleted{[text]}`	|  
| `{++[text]++}`	| `\added{[text]}`	|  
| `{~~[text1]~>[text2]~~}`	| `\replaced{[text2]}{[text1]}`	|  
| `{==[text]==}`	| `\highlight{[text]}`	|  
| `{>>[text]<<}`	| `\comment{[text]}`	|  

: Translation from CriticMarkup to LaTeX.

# Credits

- Heavily modified from [CriticMarkup Toolkit's criticParser_CLI.py](http://criticmarkup.com/services.php)
- [tests.md](tests.md) is modified from [MMD-Test-Suite/Critic.text at master · fletcher/MMD-Test-Suite](https://github.com/fletcher/MMD-Test-Suite/blob/master/CriticMarkup/Critic.text)
