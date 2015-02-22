#coding: utf-8

from unittest import TestCase, main
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
from uml_matcher.diagram import (eq_ignore_order, Diagram, MatchResult,
    Generalization)

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
        def cached_make(self):
            if self.__dict__[value_name] is None:
                self.__dict__[value_name] = make_method()
            return self.__dict__[value_name]
        cached_make.__name__ = name
        self.__dict__[name] = MethodType(cached_make, self)

class DecoratorPatternDiagramFactory(Factory):
    def __init__(self):
        def make_component(self):
            return Interface('Component', [], [Operation('operation')])

        def make_concrete_component(self):
            return Class('concrete_component()', [], [Operation('operation')])

        def make_decorator_component(self):
            return Property(Type(self.component()), 'component')

        def make_decorator(self):
            return Interface('Decorator',
                    [self.decorator_component()],
                    [Operation('operation')])

        def make_concrete_decorator(self):
            return Class('ConcreteDecorator', [], [Operation('operation')])

        def make_decorator_end(self):
            return Property(Type(self.decorator()), 'decorator end',
                aggregation=Aggregation.shared)

        def make_diagram(self):
            G = Generalization
            return Diagram(
                generalizations=[
                    G(derived=self.concrete_component(), base=self.component()),
                    G(derived=self.decorator(), base=self.component()),
                    G(derived=self.concrete_decorator(), base=self.decorator()),
                ],
                associations=[
                    {self.decorator_component(), self.decorator_end()},
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

        def make_cutlet(self):
            return Class('Cutlet', [],
                [Operation('price', result=Type(IntType))])

        def make_cheese(self):
            return Class('Cheese', [],
                [Operation('price', result=Type(IntType))])

        def make_burger(self):
            return Class('Burger', [],
                [Operation('price', result=Type(IntType))])

        def make_hamburger_cutlet(self):
            return Property(Type(self.cutlet()), 'cutlet')

        def make_hamburger(self):
            return Class('Hamburger',
                [self.hamburger_cutlet()],
                [Operation('price', result=Type(IntType))])

        def make_cheeseburger_cutlet(self):
            return Property(Type(self.cutlet()), 'cutlet')

        def make_cheeseburger_cheese(self):
            return Property(Type(self.cheese()), 'cheese')

        def make_cheeseburger(self):
            return Class('Cheeseburger',
                [self.cheeseburger_cutlet(), self.cheeseburger_cheese()],
                [Operation('price', result=Type(IntType))])

        def make_burger_with_burger(self):
            return Property(Type(self.burger()), 'burger')

        def make_burger_with(self):
            return Class('Burger with',
                [self.burger_with_burger()],
                [Operation('price', result=Type(IntType))])

        def make_burger_with_end_1(self):
            return Property(Type(self.burger_with()), 'burger_with end 1',
                aggregation=Aggregation.shared)

        def make_hamburger_end_1(self):
            return Property(Type(self.hamburger()), 'hamburger end 1',
                aggregation=Aggregation.shared)

        def make_cheeseburger_end_1(self):
            return Property(Type(self.cheeseburger()), 'cheeseburger end 1',
                aggregation=Aggregation.shared)

        def make_cheeseburger_end_2(self):
            return Property(Type(self.cheeseburger()), 'cheeseburger end 2',
                aggregation=Aggregation.shared)

        def make_diagram(self):
            G = Generalization
            return Diagram(
                generalizations=[
                    G(derived=self.cutlet(), base=self.burger_with()),
                    G(derived=self.cheese(), base=self.burger_with()),
                    G(derived=self.burger_with(), base=self.burger()),
                    G(derived=self.hamburger(), base=self.burger()),
                    G(derived=self.cheeseburger(), base=self.burger()),
                ],
                associations=[
                    {self.burger_with_burger(), self.burger_with_end_1()},
                    {self.hamburger_cutlet(), self.hamburger_end_1()},
                    {self.cheeseburger_cutlet(), self.cheeseburger_end_1()},
                    {self.cheeseburger_cheese(), self.cheeseburger_end_2()},
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
            make_burger_with_end_1,
            make_hamburger_end_1,
            make_cheeseburger_end_1,
            make_cheeseburger_end_2,
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
                    (t.hamburger_end_1(), p.decorator_end()),
                    (t.hamburger_cutlet(), p.decorator_component()),
                ],
                [
                    (t.cheeseburger_end_1(), p.decorator_end()),
                    (t.cheeseburger_cutlet(), p.decorator_component()),
                ],
                [
                    (t.cheeseburger_end_2(), p.decorator_end()),
                    (t.cheeseburger_cheese(), p.decorator_component()),
                ],
                [
                    (t.burger_with_end_1(), p.decorator_end()),
                    (t.burger_with_burger(), p.decorator_component()),
                ],
            ],
        )
        match_result = t.diagram().match(p.diagram())
        assert_that(match_result, equal_to(expected_match_result))

if __name__ == '__main__':
    main()
