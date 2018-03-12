from __future__ import print_function

import argparse
import os
import sys

from .filters import criticmarkup_accept_filter, criticmarkup_reject_filter, criticmarkup_tex_diff_filter, criticmarkup_html_diff_filter, markdown_filter, pandoc_filter, html_filter

from .version import __version__


def IO_to_format(output):
    ext = os.path.splitext(output.name)[1][1:]
    if ext == 'md':
        return 'markdown'
    elif ext == 'tex':
        return 'latex'
    else:
        return ext


def main(args):
    body = args.input.read()

    # diff/markup mode
    if args.critic_mode[0] in ('d', 'm'):
        if args.to == 'latex':
            body = criticmarkup_tex_diff_filter(body)
        # for any other format, use HTML (many formats support inline HTML)
        else:
            body = criticmarkup_html_diff_filter(body)
    # accept mode
    elif args.critic_mode[0] == 'a':
        body = criticmarkup_accept_filter(body)
    # reject mode
    elif args.critic_mode[0] == 'r':
        body = criticmarkup_reject_filter(body)
    else:
        print('Unknown critic mode {}.'.format(args.critic_mode), file=sys.stderr)

    # only convert markdown to html or tex if the output extension is really that format
    output_format = IO_to_format(args.output)
    if args.from_format == 'markdown' and output_format == 'html' and args.engine in ('markdown', 'markdown2'):
        body = markdown_filter(body, args.engine)
        body = html_filter(body, args.critic_template, args.critic_mode[0], args.standalone)
    elif output_format != args.from_format:
        # defer standalone to pandoc
        body = html_filter(body, args.critic_template, args.critic_mode[0], False)
        body = pandoc_filter(body, args.from_format, output_format, args.standalone, args.engine)
    else:
        body = html_filter(body, args.critic_template, args.critic_mode[0], args.standalone)

    args.output.write(body)


def get_args():

    parser = argparse.ArgumentParser(description='Convert Critic Markup.')

    parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file. Default: stdin.')
    # TODO: handle binary output through pypandoc: ("odt", "docx", "epub", "epub3", "pdf")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file. Default: stdout.')

    parser.add_argument('-t', '--to',
                        help='Output format. Default: inferred from --output.')
    parser.add_argument('-f', '--from', dest='from_format',
                        help='Input format. Default: inferred from --input.')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Output standalone html.')

    parser.add_argument('--critic-template', type=argparse.FileType('r'),
                        help='Custom template of CSS and JS for CriticMarkup in diff mode.')
    # parser.add_argument('--print-default-critic-template', type=argparse.FileType('w'), default=sys.stdout,
    #                     help='Custom template of CSS and JS for CriticMarkup in diff mode.')
    parser.add_argument('--engine', default='markdown',
                        help='If specified, convert markdown to HTML using the specified engine. Default: markdown. Valid: markdown, markdown2, panflute, pypandoc.')

    parser.add_argument('-m', '--critic-mode', default='diff',
                        help='Specify critic mode. Default: diff. Valid: a/accept, r/reject, d/diff, m/markup.')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    args = parser.parse_args()

    if not args.to:
        args.to = IO_to_format(args.output)
    if not args.from_format:
        args.from_format = IO_to_format(args.input)
    return args


def cli():
    main(get_args())
