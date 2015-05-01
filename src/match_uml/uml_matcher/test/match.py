# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from itertools import permutations
from uml_matcher.match import eq_ignore_order


class EqIgnoreOrder(TestCase):
    def test_compare_empty_should_be_equal(self):
        assert_that(eq_ignore_order([], []), equal_to(True))

    def test_compare_empty_to_not_empty_should_be_not_equal(self):
        assert_that(eq_ignore_order([], [1]), equal_to(False))
        assert_that(eq_ignore_order([1], []), equal_to(False))

    def test_compare_different_len_should_be_not_equal(self):
        assert_that(eq_ignore_order([1, 2, 3], [1, 2]), equal_to(False))

    def test_compare_equal_should_be_equal(self):
        assert_that(eq_ignore_order([1, 2, 3], [1, 2, 3]), equal_to(True))

    def test_compare_values_with_all_permutations_should_be_equal(self):
        values = [1, 2, 3]
        for p in permutations(values):
            assert_that(eq_ignore_order(values, p), equal_to(True))

    def test_compare_nested_tuples_equal_should_be_equal(self):
        assert_that(eq_ignore_order([(1, 2), (3, 2)], [(3, 2), (1, 2)]),
                    equal_to(True))

    def test_compare_twice_nested_tuples_equal_should_be_equal(self):
        assert_that(eq_ignore_order([[(1, 2), (2, 3)], [(3, 4), (4, 5)]],
                    [[(3, 4), (4, 5)], [(2, 3), (1, 2)]]), equal_to(True))

if __name__ == '__main__':
    main()
