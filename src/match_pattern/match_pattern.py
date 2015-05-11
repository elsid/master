#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from copy import deepcopy
from sys import stderr
from os.path import isfile
from java_parser import make_model
from patterns import make_pattern


def main():
    args = parse_args()
    target = make_target_model(args)
    pattern = make_pattern_model(args, target)
    print target.match(pattern, args.limit)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('target', type=str)
    parser.add_argument('pattern', type=str)
    parser.add_argument('-p', '--path', dest='external_path_list',
                        action='append', default=[])
    parser.add_argument('-b', '--builtin_target', action='store_true',
                        default=False)
    parser.add_argument('-e', '--external_pattern', action='store_true',
                        default=False)
    parser.add_argument('-l', '--limit', type=int, default=None)
    return parser.parse_args()


def make_target_model(args):
    if args.builtin_target:
        return make_pattern(args.target)
    else:
        return load_model(args.target, args.external_path_list)


def make_pattern_model(args, target):
    if (args.target == args.pattern
            and args.builtin_target != args.external_pattern):
        return deepcopy(target)
    else:
        if args.external_pattern:
            return load_model(args.pattern, args.external_path_list)
        else:
            return make_pattern(args.pattern)


def load_model(source, external_path_list):
    if isfile(source) and source.endswith('.yaml'):
        return yaml.load(open(source))
    model, errors = make_model(dirs=[source],
                               external_path_list=external_path_list)
    if errors:
        print >> stderr, '\n%s errors:\n' % source
    for error in errors:
        print >> stderr, str(error)
    return model


if __name__ == '__main__':
    main()
