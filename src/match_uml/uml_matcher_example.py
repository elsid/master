#!/usr/bin/env python
# coding: utf-8


from uml_matcher.test.diagram import Decorator, Burgers


if __name__ == '__main__':
    pattern = Decorator().diagram()
    target = Burgers().diagram()
    print '\npattern\n\n', pattern
    print '\ntarget\n\n', target
    print '\nmatch\n\n', target.match(pattern)
