#!/usr/bin/env python
# coding: utf-8


from uml_matcher.test.diagram import Decorator, Target


if __name__ == '__main__':
    pattern = Decorator().diagram()
    target = Target().diagram()
    print '\npattern\n\n', pattern
    print '\ntarget\n\n', target
    print '\nmatch\n\n', target.match(pattern)
