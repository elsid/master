#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from sys import stderr
from os.path import isfile
from java_parser import make_model
from pattern_matcher import Model
from patterns import make_pattern


def main():
    args = parse_args()
    target = load_model(args.path, args.external_path_list)
    pattern = make_pattern(args.pattern)
    print target.match(pattern, args.limit, args.all_components)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('pattern', type=str)
    parser.add_argument('path', type=str, nargs='+')
    parser.add_argument('-p', '--path', dest='external_path_list',
                        action='append', default=[])
    parser.add_argument('-l', '--limit', type=int, default=None)
    parser.add_argument('-a', '--all_components', action='store_true',
                        default=False)
    return parser.parse_args()


def load_model(path_list, external_path_list):
    if (len(path_list) == 1 and isfile(path_list[0])
            and path_list[0].endswith('.yaml')):
        model = yaml.load(open(path_list[0]))
        if not isinstance(model, Model):
            raise InvalidYamlFormat(path_list[0])
        return model
    model, errors = make_model(path_list=path_list,
                               external_path_list=external_path_list)
    if errors:
        print >> stderr, '\n%s errors:\n' % ','.join(path_list)
    for error in errors:
        print >> stderr, str(error)
    return model


class InvalidYamlFormat(Exception):
    def __init__(self, file_path):
        self.file_path = file_path

    def __str__(self):
        return 'invalid yaml format of file: "%s"' % self.file_path


if __name__ == '__main__':
    main()
