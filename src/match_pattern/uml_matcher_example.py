#!/usr/bin/env python
# coding: utf-8


from pattern_matcher.test.model import Decorator, Burgers


if __name__ == '__main__':
    pattern = Decorator().create()
    target = Burgers().create()
    print '\npattern\n\n', pattern
    print '\ntarget\n\n', target
    print '\nmatch\n\n', target.match(pattern)
