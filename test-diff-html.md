---
usepackage: [color,soul]
---  
  
# Definition #

- Deletions: This is ~~is~~ a test.
- Additions: This <ins>is </ins>a test.
- Substitutions: This ~~isn't~~<ins>is</ins> a test.
- Highlighting: This is a <mark>test</mark>.
- Comments: This is a test<!-- What is it a test of? -->.

# Mapping #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `~~[text]~~`	| `~~[text]~~`	| `~~[text]~~`	|  
| `<ins>[text]</ins>`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `~~[text1]~~<ins>[text2]</ins>`	| `~~[text1]~~<ins>[text2]</ins>`	| `~~[text1]~~\underline{[text2]}`	| 
| `<mark>[text]</mark>`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `<!-- [text] -->`	| `<!-- [text] -->`	| `<!-- [text] -->`	| 
