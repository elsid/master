# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to
from types import MethodType
from graph_matcher import Equivalent
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
from uml_matcher.interface import Interface
from uml_matcher.operation import Operation
from uml_matcher.property import Property
from uml_matcher.type import Type
from uml_matcher.primitive_type import PrimitiveType
from uml_matcher.aggregation import Aggregation
from uml_matcher.diagram import Diagram, Generalization, BinaryAssociation
from uml_matcher.match import MatchResult, MatchVariant


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
            return Class('ConcreteComponent', [],
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

        super(DecoratorPatternDiagramFactory, self).__init__([
            make_component,
            make_concrete_component,
            make_decorator_component,
            make_decorator,
            make_concrete_decorator,
            make_decorator_end,
            make_diagram,
        ])

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


class TargetDiagramFactory(Factory):
    def __init__(self):
        int_type = Type(PrimitiveType('int'))

        def make_cutlet(_):
            return Class('Cutlet', [], [Operation(int_type, 'price')])

        def make_cutlet_type(this):
            return Type(this.cutlet())

        def make_cheese(_):
            return Class('Cheese', [], [Operation(int_type, 'price')])

        def make_cheese_type(this):
            return Type(this.cheese())

        def make_burger(_):
            return Class('Burger', [], [Operation(int_type, 'price')])

        def make_burger_type(this):
            return Type(this.burger())

        def make_hamburger_cutlet(this):
            return Property(this.cutlet_type(), 'cutlet')

        def make_hamburger(this):
            return Class('Hamburger', [this.hamburger_cutlet()],
                         [Operation(int_type, 'price')])

        def make_hamburger_type(this):
            return Type(this.hamburger())

        def make_cheeseburger_cutlet(this):
            return Property(this.cutlet_type(), 'cutlet')

        def make_cheeseburger_cheese(this):
            return Property(this.cheese_type(), 'cheese')

        def make_cheeseburger(this):
            return Class(
                'Cheeseburger',
                [this.cheeseburger_cutlet(), this.cheeseburger_cheese()],
                [Operation(int_type, 'price')])

        def make_cheeseburger_type(this):
            return Type(this.cheeseburger())

        def make_burger_with_burger(this):
            return Property(this.burger_type(), 'burger')

        def make_burger_with(this):
            return Class('BurgerWith', [this.burger_with_burger()],
                         [Operation(int_type, 'price')])

        def make_burger_with_type(this):
            return Type(this.burger_with())

        def make_burger_with_end(this):
            return Property(this.burger_with_type(), 'BurgerWith_end',
                            aggregation=Aggregation.shared)

        def make_hamburger_end(this):
            return Property(this.hamburger_type(), 'Hamburger_end',
                            aggregation=Aggregation.shared)

        def make_cheeseburger_end(this):
            return Property(this.cheeseburger_type(), 'Cheeseburger_end',
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

        super(TargetDiagramFactory, self).__init__([
            make_cutlet,
            make_cutlet_type,
            make_cheese,
            make_cheese_type,
            make_burger,
            make_burger_type,
            make_hamburger_cutlet,
            make_hamburger,
            make_hamburger_type,
            make_cheeseburger_cutlet,
            make_cheeseburger_cheese,
            make_cheeseburger,
            make_cheeseburger_type,
            make_burger_with_burger,
            make_burger_with,
            make_burger_with_type,
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
