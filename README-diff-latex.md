---
usepackage: [color,soul]
---  

Using CriticMarkup with pandoc---not a filter but a preprocessor.

# Definition #

- Deletions: This is \st{is }a test.
- Additions: This \underline{is }a test.
- Substitutions: This \st{isn't}\underline{is} a test.
- Highlighting: This is a \hl{test}.
- Comments: This is a test\marginpar{What is a test for?}.

# Mapping #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `\st{[text]}`	| `<del>[text]</del>`	| `\sout{[text]}`	|  
| `\underline{[text]}`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `\st{[text1]}\underline{[text2]}`	| `<del>[text1]</del><ins>[text2]</ins>`	| `\sout{[text1]}\underline{[text2]}`	| 
| `\hl{[text]}`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `\marginpar{[text]}`	| `<aside>[text]</aside>`	| `\marginpar{[text]}`	| 
