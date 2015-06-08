#!/usr/bin/env python
# coding: utf-8

import re

from sys import stdout, stdin


def main():
    for line in stdin:
        if '::' in line:
            line = re.sub(r'^[^:]*::', '', line).replace('::', '.')
            if len(line) > 81:
                line = line[:79] + '\n' + line[79:]
        stdout.write(line)


if __name__ == '__main__':
    main()
