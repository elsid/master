#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from match_uml import make_target_diagram


def main():
    args = parse_args()
    diagram = make_target_diagram(args)
    print yaml.dump(diagram)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('target', type=str)
    parser.add_argument('-p', '--path', dest='external_path_list',
                        action='append', default=[])
    parser.add_argument('-b', '--builtin', action='store_true',
                        default=False, dest='builtin_target')
    return parser.parse_args()


if __name__ == '__main__':
    main()
