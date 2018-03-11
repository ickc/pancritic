from __future__ import print_function

import re
import sys

from pancritic.template import HEAD, BODY_BEGIN, BODY_END

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


def tex_filter(body, engine, standalone):
    extra_args = ['-s'] if standalone else None

    if engine == 'panflute':
        try:
            from panflute import convert_text
            return convert_text(body, output_format='latex', extra_args=extra_args)
        except:
            print('Cannot use {}, use pypandoc instead.'.format(engine), file=sys.stderr)

    try:
        from pypandoc import convert_text
        return convert_text(body, 'latex', format='markdown', extra_args=extra_args)
    except:
        print('Cannot use {}, stop converting to tex and output markdown instead.'.format(engine), file=sys.stderr)

    return body


def html_filter(body, css, standalone=False):
    if standalone:
        return HEAD + css + BODY_BEGIN + body + BODY_END
    else:
        return css + '<div id="wrapper">\n\n' + body + '\n\n</div>\n'
