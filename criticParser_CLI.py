#!/usr/bin/env python

'''
Input is quoted UNIX type file path.

Output is HTML formated text using ins, del, and aside tags

File is written to the same directory as the source unless specified with the -o flag

-m2     Uses the markdown2 module

-o <file_path>    Writes file to specified path. Must include file name

-b Opens the output HTML file in the defualt browser
'''

from __future__ import print_function

import argparse
import os
import re
import subprocess
import sys

ADD_PATTERN = r'''(?s)\{\+\+(?P<value>.*?)\+\+[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

DEL_PATTERN = r'''(?s)\{\-\-(?P<value>.*?)\-\-[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

COMM_PATTERN = r'''(?s)\{\>\>(?P<value>.*?)\<\<\}'''

SUBS_PATTERN = r'''(?s)\{\~\~(?P<original>(?:[^\~\>]|(?:\~(?!\>)))+)\~\>(?P<new>(?:[^\~\~]|(?:\~(?!\~\})))+)\~\~\}'''

MARK_PATTERN = r'''(?s)\{\=\=(?P<value>.*?)\=\=\}\{\>\>(?P<comment>.*?)\<\<\}'''

CSS = '''<style>
	#wrapper {
		padding-top: 30px !important;
	}

	#criticnav {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		box-shadow: 0 1px 1px 1px #777;
		margin: 0;
		padding: 0;
		background-color: white;
		font-size: 12px;
	}

	#criticnav ul {
		list-style-type: none;
		width: 90%;
		margin: 0 auto;
		padding: 0;
	}

	#criticnav ul li {
		display: block;
		width: 33%;
		text-align: center;
		padding: 10px 0 5px!important;
		margin: 0 !important;
		line-height: 1em;
		float: left;
		border-left: 1px solid #ccc;
		text-transform: uppercase;
	}

	#criticnav ul li:before {
		content: none !important;
	}

	#criticnav ul li#edited-button {
		border-right: 1px solid #ccc;
	}

	#criticnav ul li.active {
		background-image: -webkit-linear-gradient(top, white, #cccccc)
	}

	.original del {
			text-decoration: none;
	}	

	.original ins,
	.original span.popover,
	.original ins.break {
		display: none;
	}

	.edited ins {
			text-decoration: none;
	}	

	.edited del,
	.edited span.popover,
	.edited ins.break {
		display: none;
	}

	.original mark,
	.edited mark {
		background-color: transparent;
	}

	.markup mark {
	    background-color: #fffd38;
	    text-decoration: none;
	}

	.markup del {
	    background-color: #f6a9a9;
	    text-decoration: none;
	}

	.markup ins {
	    background-color: #a9f6a9;
	    text-decoration: none;
	}

	.markup ins.break {
		display: block;
		line-height: 2px;
		padding: 0 !important;
		margin: 0 !important;
	}

	.markup ins.break span {
		line-height: 1.5em;
	}

	.markup .popover {
		background-color: #4444ff;
		color: #fff;
	}

	.markup .popover .critic.comment {
	    display: none;
	}

	.markup .popover:hover span.critic.comment {
	    display: block;
	    position: absolute;
	    width: 200px;
	    left: 30%;
	    font-size: 0.8em; 
	    color: #ccc;
	    background-color: #333;
	    z-index: 10;
	    padding: 0.5em 1em;
	    border-radius: 0.5em;
	}

</style>

<div id="criticnav"><ul>
	<li id="markup-button">Markup</li>
	<li id="original-button">Original</li>
	<li id="edited-button">Edited</li>
</ul></div>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<script type="text/javascript">

	function critic() {

		$('#firstdiff').remove();
		$('#wrapper').addClass('markup');
		$('#markup-button').addClass('active');
		$('ins.break').unwrap();
		$('span.critic.comment').wrap('<span class="popover" />');
		$('span.critic.comment').before('&#8225;');

	}  

	function original() {
		$('#original-button').addClass('active');
		$('#edited-button').removeClass('active');
		$('#markup-button').removeClass('active');

		$('#wrapper').addClass('original');
		$('#wrapper').removeClass('edited');
		$('#wrapper').removeClass('markup');
	}

	function edited() {
		$('#original-button').removeClass('active');
		$('#edited-button').addClass('active');
		$('#markup-button').removeClass('active');

		$('#wrapper').removeClass('original');
		$('#wrapper').addClass('edited');
		$('#wrapper').removeClass('markup');
	} 

	function markup() {
		$('#original-button').removeClass('active');
		$('#edited-button').removeClass('active');
		$('#markup-button').addClass('active');

		$('#wrapper').removeClass('original');
		$('#wrapper').removeClass('edited');
		$('#wrapper').addClass('markup');
	}

	var o = document.getElementById("original-button");
	var e = document.getElementById("edited-button");
	var m = document.getElementById("markup-button");

	window.onload = critic;
	o.onclick = original;
	e.onclick = edited;
	m.onclick = markup;

</script>
'''

HEAD = '''<!DOCTYPE html>
<html>
<head>
<title>Critic Markup Output</title>'''

BODY_BEGIN = '''</head><body><div id="wrapper">'''

BODY_END = '''</div></body></html>'''


def deletionProcess(group_object):
    replaceString = ''
    if group_object.group('value') == '\n\n':
        replaceString = "<del>&nbsp;</del>"
    else:
        replaceString = '<del>' + group_object.group('value').replace("\n\n", "&nbsp;") + '</del>'
    return replaceString


def subsProcess(group_object):
    delString = '<del>' + group_object.group('original') + '</del>'
    insString = '<ins>' + group_object.group('new') + '</ins>'
    newString = delString + insString
    return newString


# Converts Addition markup to HTML
def additionProcess(group_object):
    replaceString = ''

    # Is there a new paragraph followed by new text
    if group_object.group('value').startswith('\n\n') and group_object.group('value') != "\n\n":
        replaceString = "\n\n<ins class='critic' break>&nbsp;</ins>\n\n"
        replaceString = replaceString + '<ins>' + group_object.group('value').replace("\n", " ")
        replaceString = replaceString + '</ins>'

    # Is the addition just a single new paragraph
    elif group_object.group('value') == "\n\n":
        replaceString = "\n\n<ins class='critic break'>&nbsp;" + '</ins>\n\n'

    # Is it added text followed by a new paragraph?
    elif group_object.group('value').endswith('\n\n') and group_object.group('value') != "\n\n":
        replaceString = '<ins>' + group_object.group('value').replace("\n", " ") + '</ins>'
        replaceString = replaceString + "\n\n<ins class='critic break'>&nbsp;</ins>\n\n"

    else:
        replaceString = '<ins>' + group_object.group('value').replace("\n", " ") + '</ins>'

    return replaceString


def highlightProcess(group_object):
    replaceString = '<span class="critic comment">' + group_object.group('value').replace("\n", " ") + '</span>'
    return replaceString


def markProcess(group_object):
    replaceString = '<mark>' + group_object.group('value') + '</mark><span class="critic comment">' + group_object.group('comment').replace("\n", " ") + '</span>'
    return replaceString

# filters


def criticmarkup_filter(h):
    h = re.sub(DEL_PATTERN, deletionProcess, h, flags=re.DOTALL)

    h = re.sub(ADD_PATTERN, additionProcess, h, flags=re.DOTALL)

    h = re.sub(MARK_PATTERN, markProcess, h, flags=re.DOTALL)

    # comment processing must come after highlights
    h = re.sub(COMM_PATTERN, highlightProcess, h, flags=re.DOTALL)

    return re.sub(SUBS_PATTERN, subsProcess, h, flags=re.DOTALL)


def markdown_filter(h, engine):
    def fallback():
        print('Cannot use {}, use markdown instead.'.format(engine), file=sys.stderr)

    print('Using the {} module for processing'.format(engine))

    if engine == 'markdown2':
        try:
            from markdown2 import markdown
            return markdown(h, extras=['footnotes', 'fenced-code-blocks', 'cuddled-lists', 'code-friendly'])
        except ImportError:
            fallback()

    elif engine == 'panflute':
        try:
            from panflute import convert_text
            return convert_text(h, output_format='html')
        except:
            fallback()

    elif engine == 'pypandoc':
        try:
            from pypandoc import convert_text
            return convert_text(h, 'html', format='md')
        except:
            fallback()

    elif engine != 'markdown':
            fallback()

    from markdown import markdown
    return markdown(h, extensions=['extra', 'codehilite', 'meta'])


def html_filter(h, css, standalone=False):
    if standalone:
        return HEAD + css + BODY_BEGIN + h + BODY_END
    else:
        return css + '<div id="wrapper">\n\n' + h + '</div>'


def main(args):
    h = args.input.read()

    h = criticmarkup_filter(h)

    if args.to == 'html':
        h = markdown_filter(h, args.html_engine)
    h = html_filter(h, (css_file.read() if args.css else CSS), standalone=args.standalone)

    args.output.write(h)


def cli():
    parser = argparse.ArgumentParser(description='Convert Critic Markup.')

    parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file. Default: stdin')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file. Default: sys.stdout')
    parser.add_argument('-c', '--css', type=argparse.FileType('r'),
                        help='Custom CSS file. If not specified, default CSS is used, where minimal javascript is embedded.')

    parser.add_argument('-t', '--to',
                        help='Output format. Default: inferred from --output. Valid: md, html.')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Output standalone html, only useful when output to html.')
    parser.add_argument('--html-engine', default='markdown',
                        help='If specified, convert markdown to HTML using the specified engine. Default: markdown. Valid: markdown, markdown2, panflute, pypandoc.')

    args = parser.parse_args()

    if not args.to:
        args.to = os.path.splitext(args.output.name)[1][1:]

    return args


if __name__ == "__main__":
    main(cli())
