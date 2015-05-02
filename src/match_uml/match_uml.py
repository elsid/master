#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from copy import deepcopy
from java_parser import make_diagram
from patterns import make_pattern


def main():
    args = parse_args()
    target = make_target_diagram(args)
    print '\ntarget\n'
    print target
    pattern = make_pattern_diagram(args, target)
    print '\npattern\n'
    print pattern
    print '\nmatch\n'
    print target.match(pattern, args.limit)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('target', type=str)
    parser.add_argument('pattern', type=str)
    parser.add_argument('-p', '--path', dest='external_path_list',
                        action='append', default=[])
    parser.add_argument('-b', '--builtin_target', action='store_true',
                        default=False)
    parser.add_argument('-j', '--java_pattern', action='store_true',
                        default=False)
    parser.add_argument('-l', '--limit', type=int, default=None)
    return parser.parse_args()


def make_target_diagram(args):
    if args.builtin_target:
        return make_pattern(args.target)
    else:
        return load_diagram(args.target, args.external_path_list)


def make_pattern_diagram(args, target):
    if args.target == args.pattern and args.builtin_target != args.java_pattern:
        return deepcopy(target)
    else:
        if args.java_pattern:
            return load_diagram(args.pattern, args.external_path_list)
        else:
            return make_pattern(args.pattern)


def load_diagram(source, external_path_list):
    diagram, errors = make_diagram(dirs=[source],
                                   external_path_list=external_path_list)
    if errors:
        print '\n%s errors:\n' % source
    for error in errors:
        print str(error)
    return diagram


if __name__ == '__main__':
    main()
