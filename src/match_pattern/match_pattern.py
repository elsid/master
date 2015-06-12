#!/usr/bin/env python
# coding: utf-8

import logging
import yaml
from argparse import ArgumentParser, FileType
from sys import stderr
from pattern_matcher import Model


def main():
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=verbose(args.verbose), stream=stderr,
                            format='[%(asctime)s] %(message)s')
    pattern = load_model(args.pattern)
    target = load_model(args.target)
    format_variant = OUTPUT_FORMATS[args.format]
    first = True
    for variant in target.match(pattern, args.limit):
        if first:
            first = False
            print format_variant(variant)
        else:
            print '\n%s' % format_variant(variant)


LOG_LEVEL_NAMES = (
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('target', type=FileType('r'))
    parser.add_argument('pattern', type=FileType('r'))
    parser.add_argument('-l', '--limit', type=int, default=None)
    parser.add_argument('-v', '--verbose', choices=LOG_LEVEL_NAMES)
    parser.add_argument('-f', '--format', choices=OUTPUT_FORMATS.keys(),
                        default='txt')
    return parser.parse_args()


def load_model(stream):
    model = yaml.load(stream)
    if not isinstance(model, Model):
        raise InvalidModelFormat()
    return model


def format_text(variant):
    return str(variant)


def format_dot(variant):
    return variant.as_dot().to_string()


OUTPUT_FORMATS = {
    'txt': format_text,
    'dot': format_dot,
}


class InvalidModelFormat(Exception):
    def __init__(self):
        super(InvalidModelFormat, self).__init__('invalid model format')


def verbose(level):
    return logging.getLevelName(level)


if __name__ == '__main__':
    main()
