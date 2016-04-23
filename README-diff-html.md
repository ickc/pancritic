---
usepackage: [color,soul]
---  

Using CriticMarkup with pandoc---not a filter but a preprocessor.

# Definition #

- Deletions: This is <del>is </del>a test.
- Additions: This <ins>is </ins>a test.
- Substitutions: This <del>isn't</del><ins>is</ins> a test.
- Highlighting: This is a <mark>test</mark>.
- Comments: This is a test<aside>What is a test for?</aside>.

# Mapping #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `<del>[text]</del>`	| `<del>[text]</del>`	| `\sout{[text]}`	|  
| `<ins>[text]</ins>`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `<del>[text1]</del><ins>[text2]</ins>`	| `<del>[text1]</del><ins>[text2]</ins>`	| `\sout{[text1]}\underline{[text2]}`	| 
| `<mark>[text]</mark>`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `<aside>[text]</aside>`	| `<aside>[text]</aside>`	| `\marginpar{[text]}`	| 
