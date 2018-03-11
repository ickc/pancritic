from __future__ import print_function

import argparse
import os
import sys

from pancritic.filters import criticmarkup_accept_filter, criticmarkup_reject_filter, criticmarkup_tex_diff_filter, criticmarkup_html_diff_filter, markdown_filter, tex_filter, html_filter


def output_to_format(output):
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
        if args.to in ('markdown', 'html'):
            body = criticmarkup_html_diff_filter(body)
        elif args.to == 'latex':
            body = criticmarkup_tex_diff_filter(body)
    # accept mode
    elif args.critic_mode[0] == 'a':
        body = criticmarkup_accept_filter(body)
    # reject mode
    elif args.critic_mode[0] == 'r':
        body = criticmarkup_reject_filter(body)
    else:
        print('Unknown critic mode {}.'.format(args.critic_mode), file=sys.stderr)

    # only convert markdown to html or tex if the output extension is really that format
    if output_to_format(args.output) == 'html':
        body = markdown_filter(body, args.engine)
    elif output_to_format(args.output) == 'latex':
        body = tex_filter(body, args.engine, args.standalone)

    if args.to in ('markdown', 'html'):
        body = html_filter(body, args.critic_template, args.critic_mode[0], args.standalone)

    args.output.write(body)


def get_args():

    parser = argparse.ArgumentParser(description='Convert Critic Markup.')

    parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file. Default: stdin.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file. Default: stdout.')

    parser.add_argument('-t', '--to',
                        help='Output format. Default: inferred from --output. Valid: markdown, html, latex.')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Output standalone html, only useful when output to html.')

    parser.add_argument('--critic-template', type=argparse.FileType('r'),
                        help='Custom template of CSS and JS for CriticMarkup in diff mode.')
    # parser.add_argument('--print-default-critic-template', type=argparse.FileType('w'), default=sys.stdout,
    #                     help='Custom template of CSS and JS for CriticMarkup in diff mode.')
    parser.add_argument('--engine', default='markdown',
                        help='If specified, convert markdown to HTML using the specified engine. Default: markdown. Valid: markdown, markdown2, panflute, pypandoc.')

    parser.add_argument('-m', '--critic-mode', default='diff',
                        help='Specify critic mode. Default: diff. Valid: a/accept, r/reject, d/diff, m/markup.')

    args = parser.parse_args()

    if not args.to:
        args.to = output_to_format(args.output)
    return args


def cli():
    main(get_args())


if __name__ == "__main__":
    cli()
