# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, calling, raises
from itertools import permutations
from graph_matcher import Isomorphic, CheckIsomorphismFailed
from pattern_matcher import Class, Model
from pattern_matcher.match import (
    eq_ignore_order, check, MatchVariant, MatchResult)
from pattern_matcher.cached_method import cached_method


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


class GeneralDerived(object):
    @cached_method
    def general(self):
        return Class('General')

    @cached_method
    def derived(self):
        return Class('Derived', generals=[self.general()])

    @cached_method
    def create(self):
        return Model([self.general(), self.derived()])


class Check(TestCase):
    def test_check_empty_should_succeed(self):
        assert_that(check(tuple()), equal_to(True))

    def test_check_model_with_one_generalization_should_succeed(self):
        target = GeneralDerived().create().graph()
        pattern = GeneralDerived().create().graph()
        assert_that(check([
            Isomorphic(target.get_node_by_obj_attr_value('name', 'General'),
                       pattern.get_node_by_obj_attr_value('name', 'General')),
            Isomorphic(target.get_node_by_obj_attr_value('name', 'Derived'),
                       pattern.get_node_by_obj_attr_value('name', 'Derived')),
        ]), equal_to(True))

    def test_check_model_with_one_generalization_should_return_error(self):
        t = GeneralDerived().create().graph()
        p = GeneralDerived().create().graph()

        def check_(raise_if_false=True):
            return check([
                Isomorphic(t.get_node_by_obj_attr_value('name', 'General'),
                           p.get_node_by_obj_attr_value('name', 'Derived')),
                Isomorphic(t.get_node_by_obj_attr_value('name', 'Derived'),
                           p.get_node_by_obj_attr_value('name', 'General')),
            ], raise_if_false)

        assert_that(check_(False), equal_to(False))
        assert_that(calling(check_), raises(CheckIsomorphismFailed))
        try:
            check_()
        except CheckIsomorphismFailed as error:
            assert_that(str(error), equal_to(
                "check isomorphism failed\n"
                "  Class('General') === Class('Derived') "
                "<<< Generalization (outgoing)\n"
                "  Class('Derived') === Class('General')"))


class MakeMatchVariant(TestCase):
    def test_make_empty_should_succeed(self):
        match_variant = MatchVariant()
        assert_that(str(match_variant), equal_to(''))
        assert_that(repr(match_variant), equal_to('MatchVariant()'))
        assert_that(len(match_variant), equal_to(0))

    def test_make_not_empty_should_succeed(self):
        match_variant = MatchVariant([
            Isomorphic(Class('A'), Class('B')),
            Isomorphic(Class('C'), Class('D')),
        ])
        assert_that(str(match_variant), equal_to(
            'class A === class B\n'
            'class C === class D'
        ))
        assert_that(repr(match_variant), equal_to(
            "MatchVariant([\n"
            "Isomorphic(Class('A'), Class('B')),\n"
            "Isomorphic(Class('C'), Class('D'))\n"
            "])"
        ))
        assert_that(len(match_variant), equal_to(2))


class MakeMatchResult(TestCase):
    def test_make_empty_should_succeed(self):
        match_result = MatchResult()
        assert_that(str(match_result), equal_to(''))
        assert_that(repr(match_result), equal_to('MatchResult()'))
        assert_that(len(match_result), equal_to(0))

    def test_make_not_empty_should_succeed(self):
        match_result = MatchResult([
            MatchVariant([Isomorphic(Class('A'), Class('B'))]),
            MatchVariant([
                Isomorphic(Class('C'), Class('D')),
                Isomorphic(Class('E'), Class('F')),
            ]),
        ])
        assert_that(str(match_result), equal_to(
            'class A === class B\n'
            '\n'
            'class C === class D\n'
            'class E === class F'
        ))
        assert_that(repr(match_result), equal_to(
            "MatchResult([\n"
            "MatchVariant([\n"
            "Isomorphic(Class('A'), Class('B'))\n"
            "]),\n"
            "MatchVariant([\n"
            "Isomorphic(Class('C'), Class('D')),\n"
            "Isomorphic(Class('E'), Class('F'))\n"
            "])\n"
            "])"
        ))
        assert_that(len(match_result), equal_to(2))


if __name__ == '__main__':
    main()
