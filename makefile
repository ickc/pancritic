SHELL := /usr/bin/env bash

ERRORCODE = 1

# configure engine
python := python
pip := pip
## LaTeX engine
### LaTeX workflow: pdf; xelatex; lualatex
latexmkEngine := pdf
### pandoc workflow: pdflatex; xelatex; lualatex
pandocEngine := pdflatex
## HTML
HTMLVersion := html5
## ePub
ePubVersion := epub

pancritic := pancritic
pancritic2csv := pancritic2csv

CSSURL:=https://cdn.jsdelivr.net/gh/ickc/markdown-latex-css

# command line arguments
pandocArgCommon := -f markdown+autolink_bare_uris-fancy_lists --toc -V linkcolorblue -V citecolor=blue -V urlcolor=blue -V toccolor=blue --pdf-engine=$(pandocEngine) -M date="`date "+%B %e, %Y"`"
# Workbooks
## MD
pandocArgMD := -f markdown+abbreviations+autolink_bare_uris+markdown_attribute+mmd_header_identifiers+mmd_link_attributes+mmd_title_block+tex_math_double_backslash-latex_macros-auto_identifiers -t markdown+raw_tex-native_spans-simple_tables-multiline_tables-grid_tables-latex_macros -s --wrap=none --column=999 --atx-headers --reference-location=block --file-scope
## TeX/PDF
### LaTeX workflow
latexmkArg := -$(latexmkEngine)
pandocArgFragment := $(pandocArgCommon)
### pandoc workflow
pandocArgStandalone := $(pandocArgFragment) --toc-depth=1 -s -N
## HTML/ePub
pandocArgHTML := $(pandocArgFragment) -t $(HTMLVersion) --toc-depth=2 -s -N -c $(CSSURL)/css/common.min.css -c $(CSSURL)/fonts/fonts.min.css
pandocArgePub := $(pandocArgHTML) -t $(ePubVersion) --epub-chapter-level=2
# GitHub README
pandocArgReadmeGitHub := $(pandocArgFragment) --toc-depth=2 -s -t gfm --reference-location=block
pandocArgReadmePypi := $(pandocArgFragment) -s -t rst --reference-location=block -f markdown+autolink_bare_uris-fancy_lists-implicit_header_references

testAll = tests/test-1.html tests/test-2.tex tests/test-3.tex tests/test-4.html tests/test-5.md tests/test-6.html tests/test-7.html tests/test-8.html tests/test-9.pdf
docs := $(wildcard docs/*.md)
# docsHtml := $(patsubst %.md,%.html,$(docs))
docsPdf := $(patsubst %.md,%.pdf,$(docs))
docsAll := $(docsPdf) docs/index.html README.md README.rst README.html docs/example.html docs/example.pdf

# Main Targets ########################################################################################################################################################################################

all: $(testAll) $(docsAll)
docs: $(docsAll)
readme: docs

docs/example.html: tests-ref/test.md
	pancritic $< -o $@ -s --engine panflute
docs/example.pdf: tests-ref/test.md
		pancritic $< -o docs/example.tex -s --engine panflute -m m
		latexmk -pdf docs/example.tex
		mv example.pdf $@

tests/test-5.md: tests-ref/test.md tests
	cp $< $@
	coverage run -p --branch -m pancritic $@ -i -m a
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-8.html: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -t markdown --engine pypandoc -m m | pandoc -s -o $@
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-7.html: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ -s
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-1.html: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ -m m
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-4.html: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ -s --critic-template <(echo '<div>nothing</div>')
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-6.html: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ -m r --engine markdown2
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit 1; fi
tests/test-2.tex: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ --engine pypandoc
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit $(ERRORCODE); fi
tests/test-3.tex: tests-ref/test.md tests
	coverage run -p --branch -m pancritic $< -o $@ --engine panflute
	if [[ -n $$(diff -q $@ $(subst tests,tests-ref,$@)) ]]; then cat $@; exit $(ERRORCODE); fi
# expect pancritic to override to use pypandoc
tests/test-9.pdf: tests-ref/test.md tests
	cat $< | coverage run -p --branch -m pancritic - -o $@ --engine panflute

tests:
	mkdir -p $@

test: $(testAll) # pep8
	coverage combine -a .coverage*

coverage: test
	coverage html

clean:
	rm -f .coverage* $(testAll) README.html
	rm -rf htmlcov pancritic.egg-info
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete
Clean:
	rm -f .coverage* $(testAll) $(docsAll)
	rm -rf htmlcov pancritic.egg-info
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

# Making dependancies #################################################################################################################################################################################

%.pdf: %.md $(pancritic)
	pandoc $(pandocArgStandalone) -o $@ $<
%.html: %.md $(pancritic)
	pandoc $(pandocArgHTML) $< -o $@

# readme
## index.html
docs/index.html: docs/badges.markdown docs/README.md
	pandoc $(pandocArgHTML) $^ -o $@
## GitHub README
README.md: docs/badges.markdown docs/README.md
	printf "%s\n\n" "<!--This README is auto-generated from \`docs/README.md\`. Do not edit this file directly.-->" > $@
	pandoc $(pandocArgReadmeGitHub) $^ >> $@
## PyPI README
README.rst: docs/badges.markdown docs/README.md
	printf "%s\n\n" ".. This README is auto-generated from \`docs/README.md\`. Do not edit this file directly." > $@
	pandoc $(pandocArgReadmePypi) $^ >> $@
README.html: README.rst
	rst2html.py $< > $@

# maintenance #########################################################################################################################################################################################

# Deploy to PyPI
## by Travis, properly git tagged
pypi:
	git tag -a v$$($(python) setup.py --version) -m 'Deploy to PyPI' && git push origin v$$($(python) setup.py --version)
## Manually
pypiManual:
	$(python) setup.py sdist upload || twine upload dist/*

dev:
	$(pip) install -e .[test]

pytest: $(testNative) tests/test_idempotent.native
	$(python) -m pytest -vv --cov=pancritic tests
pytestLite:
	$(python) -m pytest -vv --cov=pancritic tests
# check python styles
pep8:
	pycodestyle . --ignore=E402,E501,E731
pep8Strict:
	pycodestyle .
pyflakes:
	pyflakes .
flake8:
	flake8 .
pylint:
	pylint pancritic

# cleanup python
autopep8:
	autopep8 . --recursive --in-place --pep8-passes 2000 --verbose
autopep8Aggressive:
	autopep8 . --recursive --in-place --pep8-passes 2000 --verbose --aggressive --aggressive
