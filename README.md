---
title: Using CriticMarkup with pandoc
author: Kolen Cheung
fontfamily: lmodern,color,soul
...

Using CriticMarkup with pandoc. It serves both as a wrapper and a pre-processor.

# Definition of CriticMarkup

- Deletions: This is {--is --}a test.
- Additions: This {++is ++}a test.
- Substitutions: This {~~isn't~>is~~} a test.
- Highlighting: This is a {==test==}.
- Comments: This is a test{>>What is a test for?<<}.

# Usage: pancritic as a markdown wrapper (including but not limited to pandoc)

TODO

## Advanced Usage: pancritic as a pandoc preprocessor

TODO

# Caveats

Nesting CriticMarkup might have unexpected behavior, especially in LaTeX output. See [the caveats section in the spec of CriticMarkup](http://criticmarkup.com/spec.php#caveats).

## LaTeX Ouptut

Note that the LaTeX output requires the LaTeX packages `color` and `soul`.

One can achieve this by either using a custom template or `--include-in-header` option. Or you can use the trick of putting the following in your YAML front matter, like this file:

```yaml
---
fontfamily: lmodern,color,soul
...
```

Markdown within the CriticMarkup will not be rendered in LaTeX output. If you want to change this behavior, you can take a look at: [LaTeX Argument Parser](https://gist.github.com/mpickering/f1718fcdc4c56273ed52).

| CriticMarkup	| LaTeX	|  
| ------------------------------------------	| ----------------------------------------------	|  
| `{--[text]--}`	| `\st{[text]}`	|  
| `{++[text]++}`	| `\underline{[text]}`	|  
| `{~~[text1]~>[text2]~~}`	| `\st{[text1]}\underline{[text2]}`	|  
| `{==[text]==}`	| `\hl{[text]}`	|  
| `{>>[text]<<}`	| `\marginpar{[text]}`	|  

: Translation from CriticMarkup to LaTeX.

# Credits

- Heavily modified from [CriticMarkup Toolkit's criticParser_CLI.py](http://criticmarkup.com/services.php)
- [test.md](test.md) is modified from [MMD-Test-Suite/Critic.text at master · fletcher/MMD-Test-Suite](https://github.com/fletcher/MMD-Test-Suite/blob/master/CriticMarkup/Critic.text)
