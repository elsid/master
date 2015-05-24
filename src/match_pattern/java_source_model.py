#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from sys import stdout, stderr
from java_source_parser import make_model


def main():
    args = parse_args()
    model = load_model(args.path, args.external_path_list)
    yaml.dump(model, stdout)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('path', type=str, nargs='+')
    parser.add_argument('-p', '--path', dest='external_path_list',
                        action='append', default=[])
    return parser.parse_args()


def load_model(path_list, external_path_list):
    model, errors = make_model(path_list=path_list,
                               external_path_list=external_path_list)
    if errors:
        print >> stderr, '\n%s errors:\n' % ','.join(path_list)
    for error in errors:
        print >> stderr, str(error)
    return model


if __name__ == '__main__':
    main()
