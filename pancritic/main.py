from __future__ import print_function

import argparse
import os
import sys

from .filters import criticmarkup_accept_filter, criticmarkup_reject_filter, criticmarkup_tex_diff_filter, criticmarkup_html_diff_filter, markdown_filter, pandoc_filter, html_filter

from .version import __version__


def normalize_format(ext):
    if ext == 'md':
        return 'markdown'
    elif ext == 'tex':
        return 'latex'
    else:
        return ext


def main(args, body, output_format, is_binary):
    # parse CritiMarkup
    # diff/markup mode
    if args.critic_mode[0] in ('d', 'm'):
        if args.to in ('latex', 'pdf'):
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

    # convert between to and from format
    # only convert markdown to html or tex if the output extension is really that format
    if args.from_format == 'markdown' and output_format == 'html' and args.engine in ('markdown', 'markdown2'):
        body = markdown_filter(body, args.engine)
        body = html_filter(body, args.critic_template, args.critic_mode[0], args.standalone)
    elif output_format != args.from_format:
        # as long as the final format will be latex, don't add html_filter
        if args.to not in ('latex', 'pdf'):
            # defer standalone to pandoc
            body = html_filter(body, args.critic_template, args.critic_mode[0], False)
        if is_binary:
            # only pypandoc handles binary output
            body = pandoc_filter(body, args.from_format, output_format, args.standalone, 'pypandoc', outputfile=args.output)
        else:
            body = pandoc_filter(body, args.from_format, output_format, args.standalone, args.engine)
    elif args.to != 'latex':
        body = html_filter(body, args.critic_template, args.critic_mode[0], args.standalone)

    # write (if is binary, already written above)
    if not is_binary:
        args.output.write(body)


def get_args():
    parser = argparse.ArgumentParser(description='Convert Critic Markup.')

    parser.add_argument('input', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file. Default: stdin.')
    parser.add_argument('-o', '--output',
                        help='Output file. Default: stdout.')

    parser.add_argument('-t', '--to',
                        help='Output format. Default: inferred from --output.')
    parser.add_argument('-f', '--from', dest='from_format',
                        help='Input format. Default: inferred from --input.')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help='Output standalone html.')

    parser.add_argument('-i', '--inplace', action='store_true',
                        help='Overwrite original file.')

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

    # from-format (args.input is a file descriptor)
    if not args.from_format:
        if args.input.name != '<stdin>':
            args.from_format = normalize_format(os.path.splitext(args.input.name)[1][1:])
        else:
            print("No input file extension nor from-format specified. Default to markdown.")
            args.from_format = 'markdown'

    body = args.input.read()

    if args.inplace:
        if args.input.name == '<stdin>':
            print('Cannot perform inplace to stdin!', file=sys.stderr)
            exit(1)
        else:
            args.output = args.input.name

    args.input.close()
    

    # output-format (remember args.output is a string)
    try:
        output_format = normalize_format(os.path.splitext(args.output)[1][1:])
    except TypeError:
        print("No output file extension nor to-format specified. Default to HTML.")
        output_format = 'html'

    if args.to is None:
        args.to = output_format

    is_binary = output_format in ("odt", "docx", "epub", "epub3", "pdf")

    if not is_binary:
        args.output = sys.stdout if args.output is None else open(args.output, 'w')
    elif args.output is None:
        print('Cannot output binary format to stdout', file=sys.stderr)
        exit(1)

    return args, body, output_format, is_binary


def cli():
    main(*get_args())
