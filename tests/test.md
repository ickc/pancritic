---
title: Test CriticMarkup with pandoc
author: Kolen Cheung
fontfamily: lmodern,color,soul
---

Cum sociis natoque {--penatibus et magnis--}{>>FTP - 2013-05-13 08:20:18<<} dis parturient montes, nascetur ridiculus mus. Praesent et tellus in eros {++cunning ++}{>>FTP - 2013-05-13 08:20:22<<}eleifend imperdiet non at magna. Nunc aliquam accumsan auctor. In vitae mi sapien. Ut eget pretium purus. {~~Proin~>Prawn~~}{>>FTP - 2013-05-13 08:20:29<<} condimentum hendrerit risus quis tristique. Cras fermentum, diam id sodales feugiat, arcu risus imperdiet nisi, sit amet consequat diam lectus id mi. Cras varius convallis turpis, in iaculis mi cursus vitae. Nulla dignissim aliquet nulla, eu pulvinar nunc fringilla ut. Nullam {==condimentum tortor==}{>>Huh?<<} eu quam tempor tempus. Quisque sit amet magna nec nisl mollis varius a nec ligula. Sed adipiscing, est in gravida sagittis, elit sapien vestibulum quam, a {>>Test comment.<<}tristique arcu eros nec enim. Morbi euismod velit eget ligula faucibus quis feugiat massa fermentum. In velit tellus, pretium ac posuere ac, ultrices eget magna.

1. {++This is an *addition*.++}
2. {--This was a *deletion*.--}
3. This {~~*was*~>*is*~~} a substitution.
4. This is a {==*highlight*==}{>> With a *comment* that should not appear.<<}.
5. This is a {==*highlight*==} without comment.
