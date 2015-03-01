# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to
from types import MethodType
from itertools import permutations
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
from uml_matcher.interface import Interface
from uml_matcher.operation import Operation
from uml_matcher.property import Property
from uml_matcher.type import Type
from uml_matcher.primitive_type import PrimitiveType
from uml_matcher.aggregation import Aggregation
from uml_matcher.diagram import (
    eq_ignore_order, Diagram, MatchResult, Generalization, BinaryAssociation)


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


class Factory(object):
    def __init__(self, makes):
        for make in makes:
            self.add_method(make)

    def add_method(self, make):
        name = make.__name__.replace('make_', '')
        make_method_name = '__%s' % make.__name__
        make.__name__ = make_method_name
        make_method = MethodType(make, self)
        self.__dict__[make_method_name] = make_method
        value_name = '__%s' % name
        self.__dict__[value_name] = None

        def cached_make(this):
            if this.__dict__[value_name] is None:
                this.__dict__[value_name] = make_method()
            return this.__dict__[value_name]
        cached_make.__name__ = name
        self.__dict__[name] = MethodType(cached_make, self)


class DecoratorPatternDiagramFactory(Factory):
    def __init__(self):
        def make_component(_):
            return Interface('Component', [], [Operation(None, 'operation')])

        def make_concrete_component(_):
            return Class('concrete_component()', [],
                         [Operation(None, 'operation')])

        def make_decorator_component(this):
            return Property(Type(this.component()), 'component')

        def make_decorator(this):
            return Interface('Decorator', [this.decorator_component()],
                             [Operation(None, 'operation')])

        def make_concrete_decorator(_):
            return Class('ConcreteDecorator', [],
                         [Operation(None, 'operation')])

        def make_decorator_end(this):
            return Property(Type(this.decorator()), 'Decorator_end',
                            aggregation=Aggregation.shared)

        def make_diagram(_):
            G = Generalization
            A = BinaryAssociation
            return Diagram(
                generalizations=[
                    G(derived=self.concrete_component(), base=self.component()),
                    G(derived=self.decorator(), base=self.component()),
                    G(derived=self.concrete_decorator(), base=self.decorator()),
                ],
                associations=[
                    A({self.decorator_component(), self.decorator_end()}),
                ],
            )

        super().__init__([
            make_component,
            make_concrete_component,
            make_decorator_component,
            make_decorator,
            make_concrete_decorator,
            make_decorator_end,
            make_diagram,
        ])

    def match_result(self, other):
        G = Generalization
        return MatchResult(
            generalizations=[[
                G(derived=self.component(),
                    base=other.component()),
                G(derived=self.concrete_component(),
                    base=other.concrete_component()),
                G(derived=self.decorator(),
                    base=other.decorator()),
                G(derived=self.concrete_decorator(),
                    base=other.concrete_decorator()),
            ]],
            associations=[[
                (self.decorator_component(), other.decorator_component()),
                (self.decorator_end(), other.decorator_end()),
            ]],
        )


class TargetDiagramFactory(Factory):
    def __init__(self):
        IntType = PrimitiveType()

        def make_cutlet(_):
            return Class('Cutlet', [], [Operation(Type(IntType), 'price')])

        def make_cheese(_):
            return Class('Cheese', [], [Operation(Type(IntType), 'price')])

        def make_burger(_):
            return Class('Burger', [], [Operation(Type(IntType), 'price')])

        def make_hamburger_cutlet(this):
            return Property(Type(this.cutlet()), 'cutlet')

        def make_hamburger(this):
            return Class('Hamburger', [this.hamburger_cutlet()],
                         [Operation(Type(IntType), 'price')])

        def make_cheeseburger_cutlet(this):
            return Property(Type(this.cutlet()), 'cutlet')

        def make_cheeseburger_cheese(this):
            return Property(Type(this.cheese()), 'cheese')

        def make_cheeseburger(this):
            return Class(
                'Cheeseburger',
                [this.cheeseburger_cutlet(), this.cheeseburger_cheese()],
                [Operation(Type(IntType), 'price')])

        def make_burger_with_burger(this):
            return Property(Type(this.burger()), 'burger')

        def make_burger_with(this):
            return Class('BurgerWith', [this.burger_with_burger()],
                         [Operation(Type(IntType), 'price')])

        def make_burger_with_end(this):
            return Property(Type(this.burger_with()), 'BurgerWith_end',
                            aggregation=Aggregation.shared)

        def make_hamburger_end(this):
            return Property(Type(this.hamburger()), 'Hamburger_end',
                            aggregation=Aggregation.shared)

        def make_cheeseburger_end(this):
            return Property(Type(this.cheeseburger()), 'Cheeseburger_end',
                            aggregation=Aggregation.shared)

        def make_diagram(this):
            G = Generalization
            A = BinaryAssociation
            return Diagram(
                generalizations=[
                    G(derived=this.cutlet(), base=this.burger_with()),
                    G(derived=this.cheese(), base=this.burger_with()),
                    G(derived=this.burger_with(), base=this.burger()),
                    G(derived=this.hamburger(), base=this.burger()),
                    G(derived=this.cheeseburger(), base=this.burger()),
                ],
                associations=[
                    A({this.burger_with_burger(), this.burger_with_end()}),
                    A({this.hamburger_cutlet(), this.hamburger_end()}),
                    A({this.cheeseburger_cutlet(), this.cheeseburger_end()}),
                    A({this.cheeseburger_cheese(), this.cheeseburger_end()}),
                ],
            )

        super().__init__([
            make_cutlet,
            make_cheese,
            make_burger,
            make_hamburger_cutlet,
            make_hamburger,
            make_cheeseburger_cutlet,
            make_cheeseburger_cheese,
            make_cheeseburger,
            make_burger_with_burger,
            make_burger_with,
            make_burger_with_end,
            make_hamburger_end,
            make_cheeseburger_end,
            make_diagram,
        ])


class MatchDiagram(TestCase):
    def test_match_empty_should_has_empty_match_result(self):
        assert_that(Diagram().match(Diagram()), equal_to(MatchResult()))

    def test_match_decorator_patterns(self):
        target = DecoratorPatternDiagramFactory()
        pattern = DecoratorPatternDiagramFactory()
        expected_match_result = target.match_result(pattern)
        match_result = target.diagram().match(pattern.diagram())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_pattern_in_target(self):
        t = TargetDiagramFactory()
        p = DecoratorPatternDiagramFactory()
        G = Generalization
        expected_match_result = MatchResult(
            generalizations=[
                [
                    G(derived=t.cheeseburger(), base=p.concrete_component()),
                    G(derived=t.cutlet(), base=p.concrete_decorator()),
                    G(derived=t.burger(), base=p.component()),
                    G(derived=t.burger_with(), base=p.decorator()),
                ], [
                    G(derived=t.cutlet(), base=p.concrete_decorator()),
                    G(derived=t.burger(), base=p.component()),
                    G(derived=t.burger_with(), base=p.decorator()),
                    G(derived=t.hamburger(), base=p.concrete_component()),
                ], [
                    G(derived=t.cheeseburger(), base=p.concrete_component()),
                    G(derived=t.burger(), base=p.component()),
                    G(derived=t.burger_with(), base=p.decorator()),
                    G(derived=t.cheese(), base=p.concrete_decorator()),
                ], [
                    G(derived=t.burger(), base=p.component()),
                    G(derived=t.burger_with(), base=p.decorator()),
                    G(derived=t.cheese(), base=p.concrete_decorator()),
                    G(derived=t.hamburger(), base=p.concrete_component()),
                ],
            ],
            associations=[
                [
                    (t.hamburger_end(), p.decorator_end()),
                    (t.hamburger_cutlet(), p.decorator_component()),
                ],
                [
                    (t.cheeseburger_end(), p.decorator_end()),
                    (t.cheeseburger_cutlet(), p.decorator_component()),
                ],
                [
                    (t.cheeseburger_end(), p.decorator_end()),
                    (t.cheeseburger_cheese(), p.decorator_component()),
                ],
                [
                    (t.burger_with_end(), p.decorator_end()),
                    (t.burger_with_burger(), p.decorator_component()),
                ],
            ],
        )
        match_result = t.diagram().match(p.diagram())
        assert_that(match_result, equal_to(expected_match_result))
