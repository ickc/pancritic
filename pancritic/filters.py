from __future__ import print_function

import re
import sys

from .template import CSS, NAV, JS

ADD_EDIT = re.compile(r'(?s)\{\+\+(.*?)\+\+[ \t]*(\[(.*?)\])?[ \t]*\}')
DEL_EDIT = re.compile(r'(?s)\{\-\-(.*?)\-\-[ \t]*(\[(.*?)\])?[ \t]*\}')
COMM_EDIT = re.compile(r'(?s)\{\>\>(.*?)\<\<[ \t]*(\[(.*?)\])?[ \t]*\}')
MARK_EDIT = re.compile(r'(?s)\{\=\=(.*?)\=\=[ \t]*(\[(.*?)\])?[ \t]*\}')
SUB_EDIT = re.compile(r'''(?s)\{\~\~(?P<original>(?:[^\~\>]|(?:\~(?!\>)))+)\~\>(?P<new>(?:[^\~\~]|(?:\~(?!\~\})))+)\~\~\}''')


def criticmarkup_accept_filter(body):
    body = ADD_EDIT.sub(r'\1', body)
    body = DEL_EDIT.sub(r'', body)
    body = SUB_EDIT.sub(r'\2', body)

    body = MARK_EDIT.sub(r'\1', body)
    return COMM_EDIT.sub(r'', body)


def criticmarkup_reject_filter(body):
    body = ADD_EDIT.sub(r'', body)
    body = DEL_EDIT.sub(r'\1', body)
    body = SUB_EDIT.sub(r'\1', body)

    body = MARK_EDIT.sub(r'\1', body)
    return COMM_EDIT.sub(r'', body)


def criticmarkup_tex_diff_filter(body):
    body = ADD_EDIT.sub(r'\\underline{\1}', body)
    body = DEL_EDIT.sub(r'\\st{\1}', body)
    body = SUB_EDIT.sub(r'\\st{\1}\\underline{\2}', body)

    body = MARK_EDIT.sub(r'\\hl{\1}', body)
    return COMM_EDIT.sub(r'\\marginpar{\1}', body)


def criticmarkup_html_diff_filter(body):

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

    add_pattern = r'''(?s)\{\+\+(?P<value>.*?)\+\+[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

    del_pattern = r'''(?s)\{\-\-(?P<value>.*?)\-\-[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

    comm_pattern = r'''(?s)\{\>\>(?P<value>.*?)\<\<\}'''

    subs_pattern = r'''(?s)\{\~\~(?P<original>(?:[^\~\>]|(?:\~(?!\>)))+)\~\>(?P<new>(?:[^\~\~]|(?:\~(?!\~\})))+)\~\~\}'''

    mark_pattern = r'''(?s)\{\=\=(?P<value>.*?)\=\=\}\{\>\>(?P<comment>.*?)\<\<\}'''

    body = re.sub(del_pattern, deletionProcess, body, flags=re.DOTALL)

    body = re.sub(add_pattern, additionProcess, body, flags=re.DOTALL)

    body = re.sub(mark_pattern, markProcess, body, flags=re.DOTALL)

    # comment processing must come after highlights
    body = re.sub(comm_pattern, highlightProcess, body, flags=re.DOTALL)

    return re.sub(subs_pattern, subsProcess, body, flags=re.DOTALL)


def markdown_filter(body, engine):
    '''refactor to use pandoc_filter?
    '''
    def fallback():
        print('Cannot use {}, use markdown instead.'.format(engine), file=sys.stderr)

    if engine == 'markdown2':
        try:
            from markdown2 import markdown
            return markdown(body, extras=['footnotes', 'fenced-code-blocks', 'cuddled-lists', 'code-friendly'])
        except ImportError:
            fallback()

    elif engine == 'panflute':
        try:
            from panflute import convert_text
            return convert_text(body, output_format='html')
        except:
            fallback()

    elif engine == 'pypandoc':
        try:
            from pypandoc import convert_text
            return convert_text(body, 'html', format='md')
        except:
            fallback()

    elif engine != 'markdown':
        fallback()

    from markdown import markdown
    return markdown(body, extensions=['extra', 'codehilite', 'meta'])


def pandoc_filter(body, input_format, output_format, standalone, engine):
    extra_args = ['-s'] if standalone else None

    if engine == 'panflute':
        try:
            from panflute import convert_text
            return convert_text(body, input_format=input_format, output_format=output_format, extra_args=extra_args)
        except:
            print('Cannot use {}, use pypandoc instead.'.format(engine), file=sys.stderr)

    try:
        from pypandoc import convert_text
        return convert_text(body, output_format, input_format, extra_args=extra_args)
    except:
        print('Cannot use {}, stop converting to tex and output markdown instead.'.format(engine), file=sys.stderr)

    return body


def html_filter(body, template, mode, standalone):

    def enclose(body, value, id=None):
        return ['<{} id="{}">'.format(value, id)] + body + ['</{}>'.format(value)] if id else ['<{}>'.format(value)] + body + ['</{}>'.format(value)]

    # convert to lists
    body = [body]

    if template:
        head = [template.read()]
    elif mode == 'm':
        head = [CSS, JS]
    elif mode == 'd':
        head = [CSS, NAV, JS]
    else:
        head = []

    body = ['<!DOCTYPE html>'] + enclose(enclose(head, 'head') + enclose(enclose(body, 'div', id='wrapper'), 'body'), 'html') \
        if standalone else \
        head + enclose(body, 'div', id='wrapper')

    return '\n\n'.join(body)
