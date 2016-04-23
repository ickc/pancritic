---
usepackage: [color,soul]
---  
  
# Definition #

- Deletions: This is ~~is~~ a test.
- Additions: This \underline{is }a test.
- Substitutions: This ~~isn't~~\underline{is} a test.
- Highlighting: This is a \hl{test}.
- Comments: This is a test<!-- What is it a test of? -->.

# Mapping #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `~~[text]~~`	| `~~[text]~~`	| `~~[text]~~`	|  
| `\underline{[text]}`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `~~[text1]~~\underline{[text2]}`	| `~~[text1]~~<ins>[text2]</ins>`	| `~~[text1]~~\underline{[text2]}`	| 
| `\hl{[text]}`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `<!-- [text] -->`	| `<!-- [text] -->`	| `<!-- [text] -->`	| 
