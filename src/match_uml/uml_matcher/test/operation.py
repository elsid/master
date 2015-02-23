# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to
from uml_matcher.operation import Operation


class MakeOperation(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Operation().sub_equivalent_pattern(Operation()),
                    equal_to(True))
