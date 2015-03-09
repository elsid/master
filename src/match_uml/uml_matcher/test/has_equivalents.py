# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to
from uml_matcher.has_equivalents import has_equivalents
from uml_matcher.operation import Operation
from uml_matcher.property import Property


class HasEquivalents(TestCase):
    def test_empty_in_empty_should_found(self):
        assert_that(has_equivalents([], []), equal_to(True))

    def test_empty_in_not_empty_should_not_found(self):
        assert_that(has_equivalents([], [1]), equal_to(False))

    def test_not_empty_in_empty_should_found(self):
        assert_that(has_equivalents([1], []), equal_to(True))

    def test_one_same_should_should_found(self):
        assert_that(has_equivalents([Operation(None)], [Operation(None)]),
                    equal_to(True))

    def test_one_different_should_not_found(self):
        assert_that(has_equivalents([Property(None)], [Operation(None)]),
                    equal_to(False))

    def test_two_in_two_with_same_should_found(self):
        assert_that(has_equivalents([Property(None), Operation(None)],
                    [Property(None), Operation(None)]), equal_to(True))

    def test_one_in_two_same_should_not_found(self):
        assert_that(has_equivalents([Operation(None)],
                    [Operation(None), Operation(None)]), equal_to(False))

