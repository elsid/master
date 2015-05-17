# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, empty
from graph_matcher.configuration import Configuration, Equivalent
from graph_matcher.node import Node


class Obj(object):
    def __init__(self, str_text):
        self.str_text = str_text

    def __str__(self):
        return self.str_text

    def __repr__(self):
        return 'Obj(%s)' % repr(self.str_text)


class MakeEquivalent(TestCase):
    def test_make_should_succeed(self):
        equivalent = Equivalent(Obj('a'), Obj('b'))
        assert_that(str(equivalent), equal_to('a === b'))
        assert_that(repr(equivalent),
                    equal_to("Equivalent(Obj('a'), Obj('b'))"))


class MakeConfiguration(TestCase):
    def test_make_should_succeed(self):
        target = Node('target')
        pattern = Node('pattern')
        conf = Configuration(target, pattern, [])
        assert_that(conf.selected, equal_to([(target, pattern)]))
        assert_that(conf.checked, equal_to(set(conf.selected)))
        assert_that(conf.target(), equal_to(target))
        assert_that(conf.pattern(), equal_to(pattern))
        assert_that(conf.checked_patterns(), equal_to({pattern}))
        assert_that(conf.checked_targets(), equal_to({target}))
        assert_that(conf.at_end(), equal_to(False))
        assert_that(str(conf), equal_to("[target === pattern]"))
        assert_that(conf.advance(), equal_to(None))
        assert_that(conf.at_end(), equal_to(True))
        assert_that(str(conf), equal_to("{target === pattern}"))

if __name__ == '__main__':
    main()
