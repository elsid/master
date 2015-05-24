#!/usr/bin/env python
# coding: utf-8

import yaml
from argparse import ArgumentParser
from sys import stdout
from patterns import make_pattern, names


def main():
    args = parse_args()
    model = make_pattern(args.name)
    yaml.dump(model, stdout)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('name', choices=tuple(names()))
    return parser.parse_args()


if __name__ == '__main__':
    main()
