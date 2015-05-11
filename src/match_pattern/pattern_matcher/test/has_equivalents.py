# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from pattern_matcher.has_equivalents import has_equivalents
from pattern_matcher.operation import Operation
from pattern_matcher.property import Property


class HasEquivalents(TestCase):
    def test_empty_in_empty_should_found(self):
        assert_that(has_equivalents([], []), equal_to(True))

    def test_empty_in_not_empty_should_not_found(self):
        assert_that(has_equivalents([], [1]), equal_to(False))

    def test_not_empty_in_empty_should_found(self):
        assert_that(has_equivalents([1], []), equal_to(True))

    def test_one_same_should_should_found(self):
        assert_that(has_equivalents([Operation()], [Operation()]),
                    equal_to(True))

    def test_one_different_should_not_found(self):
        assert_that(has_equivalents([Property()], [Operation()]),
                    equal_to(False))

    def test_two_in_two_with_same_should_found(self):
        assert_that(has_equivalents([Property(), Operation()],
                    [Property(), Operation()]), equal_to(True))

    def test_one_in_two_same_should_not_found(self):
        assert_that(has_equivalents([Operation()],
                    [Operation(), Operation()]), equal_to(False))

if __name__ == '__main__':
    main()
