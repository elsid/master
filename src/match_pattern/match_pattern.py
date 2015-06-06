#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser, FileType
from pattern_matcher import Model


def main():
    args = parse_args()
    pattern = load_model(args.pattern)
    target = load_model(args.target)
    first = True
    for variant in target.match(pattern, args.limit):
        if first:
            first = False
            print '%s' % variant
        else:
            print '\n%s' % variant


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('target', type=FileType('r'))
    parser.add_argument('pattern', type=FileType('r'))
    parser.add_argument('-l', '--limit', type=int, default=None)
    return parser.parse_args()


def load_model(stream):
    model = yaml.load(stream)
    if not isinstance(model, Model):
        raise InvalidModelFormat()
    return model


class InvalidModelFormat(Exception):
    def __init__(self):
        super(InvalidModelFormat, self).__init__('invalid model format')


if __name__ == '__main__':
    main()
