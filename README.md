---
usepackage: [color,soul]
---  

Using CriticMarkup with pandoc---not a filter but a preprocessor.

# Definition #

- Deletions: This is {--is --}a test.
- Additions: This {++is ++}a test.
- Substitutions: This {~~isn't~>is~~} a test.
- Highlighting: This is a {==test==}.
- Comments: This is a test{>>What is a test for?<<}.

# Mapping #

| critic markup	| HTML	| LaTeX  	| 
|  ------------------------------------------	| -------------------------------------------------	| ----------------------------------------------	|  
| `{--[text]--}`	| `<del>[text]</del>`	| `\sout{[text]}`	|  
| `{++[text]++}`	| `<ins>[text]</ins>`	| `\underline{[text]}`	| 
| `{~~[text1]~>[text2]~~}`	| `<del>[text1]</del><ins>[text2]</ins>`	| `\sout{[text1]}\underline{[text2]}`	| 
| `{==[text]==}`	| `<mark>[text]</mark>`	| `\hl{[text]}`	| 
| `{>>[text]<<}`	| `<aside>[text]</aside>`	| `\marginpar{[text]}`	| 