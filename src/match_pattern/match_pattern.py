#!/usr/bin/env python
# coding: utf-8

import logging
import yaml
from argparse import ArgumentParser, FileType
from os.path import join, isdir
from sys import stderr
from pattern_matcher import Model


def main():
    args = parse_args()
    setup_logging(args)
    pattern = load_model(args.pattern)
    target = load_model(args.target)
    format_variant = OUTPUT_FORMATS[args.format]
    if args.dir:
        assert isdir(args.dir)
        for num, variant in enumerate(target.match(pattern, args.limit)):
            file_path = join(args.dir, '%d.%s' % (num + 1, args.format))
            open(file_path, 'w').write(format_variant(variant))
    else:
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
    parser.add_argument('-d', '--dir')
    parser.add_argument('-t', '--log_time', action='store_true')
    return parser.parse_args()


def setup_logging(args):
    if args.verbose:
        log_format = ('[%(asctime)s] ' if args.log_time else '') + '%(message)s'
        logging.basicConfig(level=verbose(args.verbose), stream=stderr,
                            format=log_format)


def load_model(stream):
    model = yaml.load(stream)
    if not isinstance(model, Model):
        raise InvalidModelFormat()
    return model


def format_text(variant):
    return str(variant)


def format_from_dot(variant, to_format='raw'):
    return variant.as_dot().create(format=to_format)


def format_yaml(variant):
    return yaml.dump([dict(target=t, pattern=p)
                      for t, p in variant.isomorphism])


OUTPUT_FORMATS = {
    'txt': format_text,
    'dot': lambda x: format_from_dot(x),
    'dot.svg': lambda x: format_from_dot(x, 'svg'),
    'yaml': format_yaml,
}


class InvalidModelFormat(Exception):
    def __init__(self):
        super(InvalidModelFormat, self).__init__('invalid model format')


def verbose(level):
    return logging.getLevelName(level)


if __name__ == '__main__':
    main()
