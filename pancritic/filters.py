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
    body = ADD_EDIT.sub(r'\\added{\1}', body)
    body = DEL_EDIT.sub(r'\\deleted{\1}', body)
    body = SUB_EDIT.sub(r'\\replaced{\2}{\1}', body)

    body = MARK_EDIT.sub(r'\\highlight{\1}', body)
    return COMM_EDIT.sub(r'\\comment{\1}', body)


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

    def markCommProcess(group_object):
        replaceString = '<mark>' + group_object.group('value') + '</mark><span class="critic comment">' + group_object.group('comment').replace("\n", " ") + '</span>'
        return replaceString

    def markProcess(group_object):
        replaceString = '<mark>' + group_object.group('value') + '</mark>'
        return replaceString

    add_pattern = r'''(?s)\{\+\+(?P<value>.*?)\+\+[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

    del_pattern = r'''(?s)\{\-\-(?P<value>.*?)\-\-[ \t]*(\[(?P<meta>.*?)\])?[ \t]*\}'''

    comm_pattern = r'''(?s)\{\>\>(?P<value>.*?)\<\<\}'''

    subs_pattern = r'''(?s)\{\~\~(?P<original>(?:[^\~\>]|(?:\~(?!\>)))+)\~\>(?P<new>(?:[^\~\~]|(?:\~(?!\~\})))+)\~\~\}'''

    mark_comm_pattern = r'''(?s)\{\=\=(?P<value>.*?)\=\=\}\{\>\>(?P<comment>.*?)\<\<\}'''

    mark_pattern = r'''(?s)\{\=\=(?P<value>.*?)\=\=\}'''

    body = re.sub(del_pattern, deletionProcess, body, flags=re.DOTALL)

    body = re.sub(add_pattern, additionProcess, body, flags=re.DOTALL)

    body = re.sub(mark_comm_pattern, markCommProcess, body, flags=re.DOTALL)

    body = re.sub(mark_pattern, markProcess, body, flags=re.DOTALL)

    # comment processing must come after highlights
    body = re.sub(comm_pattern, highlightProcess, body, flags=re.DOTALL)

    return re.sub(subs_pattern, subsProcess, body, flags=re.DOTALL)


def markdown_filter(body, engine):

    def _markdown2_filter(body):
        from markdown2 import markdown
        return markdown(body, extras=['footnotes', 'fenced-code-blocks', 'cuddled-lists', 'code-friendly'])

    def _markdown_filter(body):
        from markdown import markdown
        return markdown(body, extensions=['extra', 'codehilite', 'meta'])

    engines = ('markdown2', 'markdown') if engine == 'markdown2' else ('markdown', 'markdown2')
    engine_function = {
        'markdown': _markdown_filter,
        'markdown2': _markdown2_filter
    }

    for i, engine in enumerate(engines):
        try:
            # i != 0 means failing last time
            if i != 0:
                print('Use {} instead.'.format(engine), file=sys.stderr)
            return engine_function[engine](body)
        except:
            print('Cannot use {}.'.format(engine), file=sys.stderr)

    print('Stop converting and output original format instead.', file=sys.stderr)

    return body


def pandoc_filter(body, input_format, output_format, standalone, engine, outputfile=None):
    extra_args = ['-s'] if standalone else []

    def panflute_filter(body, input_format, output_format, extra_args, outputfile):
        from panflute import convert_text
        return convert_text(body, input_format=input_format, output_format=output_format, extra_args=extra_args)

    def pypandoc_filter(body, input_format, output_format, extra_args, outputfile):
        from pypandoc import convert_text
        return convert_text(body, output_format, input_format, extra_args=extra_args, outputfile=outputfile)

    engines = ('panflute', 'pypandoc') if engine == 'panflute' else ('pypandoc', 'panflute')
    engine_function = {
        'panflute': panflute_filter,
        'pypandoc': pypandoc_filter
    }

    for i, engine in enumerate(engines):
        try:
            # i != 0 means failing last time
            if i != 0:
                print('Use {} instead.'.format(engine), file=sys.stderr)
            return engine_function[engine](body, input_format, output_format, extra_args, outputfile)
        except:
            print('Cannot use {}.'.format(engine), file=sys.stderr)

    print('Stop converting and output original format instead.', file=sys.stderr)

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

    body = (
        ['<!DOCTYPE html>'] + enclose(enclose(head, 'head') + enclose(enclose(body, 'div', id='wrapper'), 'body'), 'html')
        if head else
        ['<!DOCTYPE html>'] + enclose(enclose(body, 'body'), 'html')
    ) if standalone else (
        head + enclose(body, 'div', id='wrapper')
        if head else
        body
    )

    return '\n\n'.join(body)
