#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from sys import stdout
from match_pattern import load_model


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


if __name__ == '__main__':
    main()
