# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, calling, raises
from itertools import permutations
from graph_matcher import Equivalent
from patterns.cached_method import cached_method
from uml_matcher import Class, Diagram, Generalization
from uml_matcher.errors import CheckVariantFailed
from uml_matcher.match import eq_ignore_order, check


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


class BaseDerivedDiagram(object):
    @cached_method
    def base(self):
        return Class('Base')

    @cached_method
    def derived(self):
        return Class('Derived')

    @cached_method
    def diagram(self):
        return Diagram(generalizations=[
            Generalization(base=self.base(), derived=self.derived()),
        ])


class Check(TestCase):
    def test_check_empty_should_succeed(self):
        check(tuple())

    def test_check_diagram_with_one_generalization_should_succeed(self):
        target = BaseDerivedDiagram().diagram().graph()
        pattern = BaseDerivedDiagram().diagram().graph()
        check([
            Equivalent(target.get_node_by_obj_attr_value('name', 'Base'),
                       pattern.get_node_by_obj_attr_value('name', 'Base')),
            Equivalent(target.get_node_by_obj_attr_value('name', 'Derived'),
                       pattern.get_node_by_obj_attr_value('name', 'Derived')),
        ])

    def test_check_diagram_with_one_generalization_should_return_error(self):
        target = BaseDerivedDiagram().diagram().graph()
        pattern = BaseDerivedDiagram().diagram().graph()
        check_ = (lambda: check([
            Equivalent(target.get_node_by_obj_attr_value('name', 'Base'),
                       pattern.get_node_by_obj_attr_value('name', 'Derived')),
            Equivalent(target.get_node_by_obj_attr_value('name', 'Derived'),
                       pattern.get_node_by_obj_attr_value('name', 'Base')),
        ]))
        assert_that(calling(check_), raises(CheckVariantFailed))
        try:
            check_()
        except CheckVariantFailed as error:
            assert_that(str(error), equal_to(
                'check variant failed\n'
                '  Base === Derived <<< Generalization (outgoing)\n'
                '  Derived === Base'))

if __name__ == '__main__':
    main()
