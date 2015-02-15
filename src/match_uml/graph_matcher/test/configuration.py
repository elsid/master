#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from graph_matcher.configuration import Configuration
from graph_matcher.node import Node

class MakeConfigurationTest(TestCase):
    def test_make_should_succeed(self):
        target = Node('target')
        pattern = Node('pattern')
        conf = Configuration(target, pattern)
        assert_that(conf.selected, equal_to([(target, pattern)]))
        assert_that(conf.current, equal_to(0))
        assert_that(conf.visited, equal_to(set(conf.selected)))
        assert_that(conf.target(), equal_to(target))
        assert_that(conf.pattern(), equal_to(pattern))
        assert_that(conf.visited_patterns(), equal_to({pattern}))
        assert_that(conf.visited_targets(), equal_to({target}))
        assert_that(conf.copy(), equal_to(conf))
        assert_that(conf.at_end(), equal_to(False))
        assert_that(conf.priority(), equal_to(1))
        assert_that(repr(conf), equal_to("[('target', 'pattern')]"))
        assert_that(conf.step(), equal_to(None))
        assert_that(conf.at_end(), equal_to(True))
        assert_that(repr(conf), equal_to("('target', 'pattern')"))

if __name__ == '__main__':
    main()
