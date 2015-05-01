# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from graph_matcher import Equivalent
from patterns import (
    AbstractFactory as AbstractFactoryPattern,
    Decorator as DecoratorPattern,
    cached_method,
)
from uml_matcher.operation import Operation
from uml_matcher.property import Property
from uml_matcher.type import Type
from uml_matcher.primitive_type import PrimitiveType
from uml_matcher.aggregation import Aggregation
from uml_matcher.diagram import Diagram, Generalization, BinaryAssociation
from uml_matcher.match import MatchResult, MatchVariant
from uml_matcher.visibility import Visibility
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class AbstractFactory(AbstractFactoryPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant(
                generalizations=(
                    Equivalent(target=self.client(), pattern=other.client()),
                    Equivalent(target=self.abstract_factory(),
                               pattern=other.abstract_factory()),
                    Equivalent(target=self.concrete_factory(),
                               pattern=other.concrete_factory()),
                    Equivalent(target=self.abstract_product(),
                               pattern=other.abstract_product()),
                    Equivalent(target=self.concrete_product(),
                               pattern=other.concrete_product()),
                ),
                dependencies=(
                    Equivalent(target=self.client(), pattern=other.client()),
                    Equivalent(target=self.abstract_factory(),
                               pattern=other.abstract_factory()),
                    Equivalent(target=self.abstract_product(),
                               pattern=other.abstract_product()),
                ),
            )
        ])


class Decorator(DecoratorPattern):
    def match_result(self, other):
        E = Equivalent
        return MatchResult([
            MatchVariant(
                generalizations=(
                    E(target=self.component(), pattern=other.component()),
                    E(target=self.concrete_component(),
                      pattern=other.concrete_component()),
                    E(target=self.decorator(), pattern=other.decorator()),
                    E(target=self.concrete_decorator(),
                      pattern=other.concrete_decorator()),
                ),
                associations=(
                    E(target=self.decorator_component(),
                      pattern=other.decorator_component()),
                    E(target=self.decorator_end(),
                      pattern=other.decorator_end()),
                ),
            )
        ])


class Target(object):
    INT_TYPE = Type(PrimitiveType('int'))

    @cached_method
    def cutlet(self):
        return Class('Cutlet', [],
                     [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def cutlet_type(self):
        return Type(self.cutlet())

    @cached_method
    def cheese(self):
        return Class('Cheese', [],
                     [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def cheese_type(self):
        return Type(self.cheese())

    @cached_method
    def burger(self):
        return Class('Burger', [],
                     [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def burger_type(self):
        return Type(self.burger())

    @cached_method
    def hamburger_cutlet(self):
        return Property(self.cutlet_type(), 'cutlet')

    @cached_method
    def hamburger(self):
        return Class('Hamburger', [self.hamburger_cutlet()],
                     [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def hamburger_type(self):
        return Type(self.hamburger())

    @cached_method
    def cheeseburger_cutlet(self):
        return Property(self.cutlet_type(), 'cutlet')

    @cached_method
    def cheeseburger_cheese(self):
        return Property(self.cheese_type(), 'cheese')

    @cached_method
    def cheeseburger(self):
        return Class(
            'Cheeseburger',
            [self.cheeseburger_cutlet(), self.cheeseburger_cheese()],
            [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def cheeseburger_type(self):
        return Type(self.cheeseburger())

    @cached_method
    def burger_with_burger(self):
        return Property(self.burger_type(), 'burger')

    @cached_method
    def burger_with(self):
        return Class('BurgerWith', [self.burger_with_burger()],
                     [Operation(self.INT_TYPE, 'price', Visibility.public)])

    @cached_method
    def burger_with_type(self):
        return Type(self.burger_with())

    @cached_method
    def burger_with_end(self):
        return Property(self.burger_with_type(), 'BurgerWith_end',
                        aggregation=Aggregation.shared)

    @cached_method
    def hamburger_end(self):
        return Property(self.hamburger_type(), 'Hamburger_end',
                        aggregation=Aggregation.shared)

    @cached_method
    def cheeseburger_end(self):
        return Property(self.cheeseburger_type(), 'Cheeseburger_end',
                        aggregation=Aggregation.shared)

    @cached_method
    def diagram(self):
        G = Generalization
        A = BinaryAssociation
        return Diagram(
            generalizations=[
                G(derived=self.cutlet(), base=self.burger_with()),
                G(derived=self.cheese(), base=self.burger_with()),
                G(derived=self.burger_with(), base=self.burger()),
                G(derived=self.hamburger(), base=self.burger()),
                G(derived=self.cheeseburger(), base=self.burger()),
            ],
            associations=[
                A({self.burger_with_burger(), self.burger_with_end()}),
                A({self.hamburger_cutlet(), self.hamburger_end()}),
                A({self.cheeseburger_cutlet(), self.cheeseburger_end()}),
                A({self.cheeseburger_cheese(), self.cheeseburger_end()}),
            ],
        )


class MatchDiagram(TestCase):
    def test_match_empty_should_has_empty_match_result(self):
        assert_that(Diagram().match(Diagram()), equal_to(MatchResult()))

    def test_match_abstract_factory_patterns(self):
        target = AbstractFactory()
        pattern = AbstractFactory()
        expected_match_result = target.match_result(pattern)
        match_result = target.diagram().match(pattern.diagram())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_patterns(self):
        target = Decorator()
        pattern = Decorator()
        expected_match_result = target.match_result(pattern)
        match_result = target.diagram().match(pattern.diagram())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_pattern_in_target(self):
        t = Target()
        p = Decorator()
        E = Equivalent
        expected_match_result = MatchResult([
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cheese(), p.concrete_decorator()),
                    E(t.cheeseburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.burger_with_end(), p.decorator_end()),
                    E(t.burger_with_burger(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cheese(), p.concrete_decorator()),
                    E(t.hamburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.burger_with_end(), p.decorator_end()),
                    E(t.burger_with_burger(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cutlet(), p.concrete_decorator()),
                    E(t.cheeseburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.burger_with_end(), p.decorator_end()),
                    E(t.burger_with_burger(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cutlet(), p.concrete_decorator()),
                    E(t.hamburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.burger_with_end(), p.decorator_end()),
                    E(t.burger_with_burger(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cheese(), p.concrete_decorator()),
                    E(t.cheeseburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.cheeseburger_end(), p.decorator_end()),
                    E(t.cheeseburger_cheese(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cutlet(), p.concrete_decorator()),
                    E(t.cheeseburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.cheeseburger_end(), p.decorator_end()),
                    E(t.cheeseburger_cutlet(), p.decorator_component()),
                ]
            ),
            MatchVariant(
                generalizations=[
                    E(t.burger(), p.component()),
                    E(t.burger_with(), p.decorator()),
                    E(t.cutlet(), p.concrete_decorator()),
                    E(t.hamburger(), p.concrete_component()),
                ],
                associations=[
                    E(t.hamburger_end(), p.decorator_end()),
                    E(t.hamburger_cutlet(), p.decorator_component()),
                ]
            ),
        ])
        match_result = t.diagram().match(p.diagram())
        assert_that(match_result, equal_to(expected_match_result))


class ReprDiagram(TestCase):
    def test_repr_empty_should_succeed(self):
        assert_that(repr(Diagram()), equal_to(''))

    def test_repr_abstract_factory_empty_should_succeed(self):
        assert_that(repr(AbstractFactory().diagram()), equal_to(
            'generalizations\n'
            '  ConcreteFactory ----> AbstractFactory\n'
            '  ConcreteProduct ----> AbstractProduct\n'
            'dependencies\n'
            '  Client - - > AbstractFactory\n'
            '  Client - - > AbstractProduct'))

    def test_repr_decorator_empty_should_succeed(self):
        assert_that(repr(Decorator().diagram()), equal_to(
            'generalizations\n'
            '  ConcreteComponent ----> Component\n'
            '  Decorator ----> Component\n'
            '  ConcreteDecorator ----> Decorator\n'
            'associations\n'
            '  Decorator_end ----- Decorator::component'))

if __name__ == '__main__':
    main()
