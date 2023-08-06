# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

import os
import sys
import argparse
import contextlib
from datetime import datetime as dt

from wa.extract import WebExtractor
from wa.utils import eprint
from wa._version import version


class Article:
    def __init__(self):
        self.title = None
        self.text = None

    @property
    def initialized(self):
        return self.title and self.text


def fetch_article(url, baseurl, fmt, dump_cmd):
    parser = WebExtractor(url, baseurl)

    art = Article()
    art.title = parser.title

    if fmt == 'text':
        art.text = parser.text
    elif fmt == 'md':
        art.text = parser.md
    elif fmt == 'html':
        art.text = parser.html
    elif fmt == 'dump':
        art.text = parser.original_dump(dump_cmd)
    else:
        raise ValueError('invalid output format: {}'.format(fmt))

    return art


def to_filename(title, fmt):
    ext_mapping = {
        'text': '.txt',
        'md': '.md',
        'html': '.html',
        'dump': '.txt'
    }

    return '{}{}'.format(
        title.strip().lower().replace(' ', '-'),
        ext_mapping[fmt])


@contextlib.contextmanager
def make_printer(args):
    if args.save:
        with open(args.save, 'w') as f_:
            yield lambda *a: print(*a, file=f_)
    else:
        yield print


def prepare_args():
    out_formats = ('html', 'md', 'text', 'dump')

    parser = argparse.ArgumentParser(
        description='Displays readable contents of web pages in various '
                    'formats.')

    parser.add_argument(
        '-t', '--to', choices=out_formats, default='text',
        help='select output format; default: text')
    parser.add_argument(
        '-s', '--save', nargs='?', const='', metavar='FILE',
        help='save the article to selected file instead of printing it to '
             'standard output; if no path is provided, deduced file name '
             'will be printed to stdout')
    parser.add_argument(
        '-T', '--title',
        help='set title of fetched article')
    parser.add_argument(
        '-m', '--front-matter', action='store_true',
        help='print YAML front matter with fetched metadata in front of '
             'article contents')
    parser.add_argument(
        '--dump-cmd', default='links -dump', metavar='CMD',
        help='command to which URL is passed when `-t dump` is used; '
             'default: links -dump')
    parser.add_argument(
        '--baseurl', metavar='URL',
        help='when webarchive\'s input is a local file or standard input, this '
            'parameter can be used to hint about the source of archived '
            'content; it is used to e.g. resolve relative links')
    parser.add_argument(
        '-f', '--force', action='store_true',
        help='forces overwriting output files')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {}'.format(version))
    parser.add_argument(
        'url',
        help='URL to be archived; can be http(s) URL, local file or a dash "-" '
             'to read contents from standard input')
    return parser.parse_args()


def main():
    args = prepare_args()

    article = fetch_article(args.url, args.baseurl, args.to, args.dump_cmd)
    if not article.initialized:
        eprint('Unable to fetch article')
        return 1

    # overwrite title
    if args.title:
        article.title = args.title

    # deduce save file path
    savepath_deduced = (args.save == '')
    if args.save == '':
        args.save = to_filename(article.title, args.to)

    if args.save and os.path.exists(args.save) and not args.force:
        eprint('File exists, refusing overwriting: "{}"'.format(args.save))
        return 1

    with make_printer(args) as printer:
        if savepath_deduced:
            print(args.save)

        if args.front_matter:
            printer('---')
            printer('title:', article.title)
            printer('date:', dt.now().replace(microsecond=0).isoformat())
            printer('---')
            printer()
        printer(article.text)

    return 0


sys.exit(main())
