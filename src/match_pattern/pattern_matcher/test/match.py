# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, calling, raises, empty
from itertools import permutations
from graph_matcher import Isomorphic, CheckIsomorphismFailed
from pattern_matcher import Class, Model
from pattern_matcher.match import (
    eq_ignore_order, check, MatchVariant, MatchResult, all_indirect_generals,
    find_overridden)
from pattern_matcher.cached_method import cached_method
from pattern_matcher.classifier import Classifier
from pattern_matcher.operation import Operation


class EqIgnoreOrder(TestCase):
    def test_compare_empty_should_be_equal(self):
        assert_that(eq_ignore_order([], []))

    def test_compare_empty_to_not_empty_should_be_not_equal(self):
        assert_that(not eq_ignore_order([], [1]))
        assert_that(not eq_ignore_order([1], []))

    def test_compare_different_len_should_be_not_equal(self):
        assert_that(not eq_ignore_order([1, 2, 3], [1, 2]))

    def test_compare_equal_should_be_equal(self):
        assert_that(eq_ignore_order([1, 2, 3], [1, 2, 3]))

    def test_compare_values_with_all_permutations_should_be_equal(self):
        values = [1, 2, 3]
        for p in permutations(values):
            assert_that(eq_ignore_order(values, p))

    def test_compare_nested_tuples_equal_should_be_equal(self):
        assert_that(eq_ignore_order([(1, 2), (3, 2)], [(3, 2), (1, 2)]))

    def test_compare_twice_nested_tuples_equal_should_be_equal(self):
        assert_that(eq_ignore_order([[(1, 2), (2, 3)], [(3, 4), (4, 5)]],
                    [[(3, 4), (4, 5)], [(2, 3), (1, 2)]]))


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
        assert_that(check(tuple()))

    def test_check_model_with_one_generalization_should_succeed(self):
        target = GeneralDerived().create().graph()
        pattern = GeneralDerived().create().graph()
        assert_that(check([
            Isomorphic(target.get_node_by_obj_attr_value('name', 'General'),
                       pattern.get_node_by_obj_attr_value('name', 'General')),
            Isomorphic(target.get_node_by_obj_attr_value('name', 'Derived'),
                       pattern.get_node_by_obj_attr_value('name', 'Derived')),
        ]))

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

        assert_that(not check_(False))
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


class AllIndirectGenerals(TestCase):
    def test_for_classifier_without_generals(self):
        assert_that(list(all_indirect_generals(Classifier('A'))), empty())

    def test_for_classifier_with_one_general(self):
        base = Classifier('Base')
        derived = Classifier('Derived', generals=[base])
        assert_that(list(all_indirect_generals(derived)), equal_to([base]))

    def test_for_classifier_with_three_generals(self):
        base1 = Classifier('Base')
        base2 = Classifier('Base')
        base3 = Classifier('Base')
        derived = Classifier('Derived', generals=[base1, base2, base3])
        assert_that(list(all_indirect_generals(derived)),
                    equal_to([base1, base2, base3]))

    def test_for_classifier_in_generalization_chain(self):
        first = Classifier('First')
        second = Classifier('Second', generals=[first])
        third = Classifier('Third', generals=[second])
        assert_that(list(all_indirect_generals(third)),
                    equal_to([second, first]))

    def test_for_classifier_in_generalization_tree(self):
        leaf1 = Classifier('Leaf1')
        leaf2 = Classifier('Leaf2')
        leaf3 = Classifier('Leaf3')
        leaf4 = Classifier('Leaf4')
        middle1 = Classifier('Middle1', generals=[leaf1, leaf2])
        middle2 = Classifier('Middle2', generals=[leaf3, leaf4])
        top = Classifier('Top', generals=[middle1, middle2])
        assert_that(list(all_indirect_generals(top)),
                    equal_to([middle1, middle2, leaf1, leaf2, leaf3, leaf4]))

    def test_for_classifier_in_diamond_generalization(self):
        leaf = Classifier('Leaf')
        middle1 = Classifier('Middle1', generals=[leaf])
        middle2 = Classifier('Middle2', generals=[leaf])
        top = Classifier('Top', generals=[middle1, middle2])
        assert_that(list(all_indirect_generals(top)),
                    equal_to([middle1, middle2, leaf]))


class FindOverridden(TestCase):
    def test_find_for_classifier_without_generals(self):
        operation = Operation('f')
        Classifier('A', operations=[operation])
        assert_that(find_overridden(operation), equal_to(None))

    def test_find_for_classifier_with_one_general(self):
        base_operation = Operation('f')
        base = Classifier('Base', operations=[base_operation])
        operation = Operation('f')
        Classifier('Derived', operations=[operation], generals=[base])
        assert_that(find_overridden(operation), equal_to(base_operation))

    def test_find_direct_in_generalization_chain(self):
        first_operation = Operation('f')
        first = Classifier('First', operations=[first_operation])
        second_operation = Operation('f')
        second = Classifier('Second', generals=[first],
                            operations=[second_operation])
        operation = Operation('f')
        Classifier('Third', generals=[second], operations=[operation])
        assert_that(find_overridden(operation), equal_to(second_operation))

    def test_find_indirect_in_generalization_chain(self):
        first_operation = Operation('f')
        first = Classifier('First', operations=[first_operation])
        second = Classifier('Second', generals=[first])
        operation = Operation('f')
        Classifier('Third', generals=[second], operations=[operation])
        assert_that(find_overridden(operation), equal_to(first_operation))


if __name__ == '__main__':
    main()
