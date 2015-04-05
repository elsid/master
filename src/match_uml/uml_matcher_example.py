#!/usr/bin/env python
# coding: utf-8


from uml_matcher.test.diagram import (
    DecoratorPatternDiagramFactory, TargetDiagramFactory)


if __name__ == '__main__':
    pattern = DecoratorPatternDiagramFactory().diagram()
    target = TargetDiagramFactory().diagram()
    print '\npattern\n\n', pattern
    print '\ntarget\n\n', target
    print '\nmatch\n\n', target.match(pattern)
