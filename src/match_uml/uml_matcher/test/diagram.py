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
from uml_matcher.diagram import Diagram
from uml_matcher.match import MatchResult, MatchVariant
from uml_matcher.visibility import Visibility
Class = __import__('uml_matcher.class', fromlist=['Class']).Class


class AbstractFactory(AbstractFactoryPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant([
                Equivalent(target=self.client(), pattern=other.client()),
                Equivalent(target=self.abstract_factory(),
                           pattern=other.abstract_factory()),
                Equivalent(target=self.concrete_factory(),
                           pattern=other.concrete_factory()),
                Equivalent(target=self.abstract_product(),
                           pattern=other.abstract_product()),
                Equivalent(target=self.concrete_product(),
                           pattern=other.concrete_product()),
                Equivalent(target=self.abstract_factory_create(),
                           pattern=other.abstract_factory_create()),
                Equivalent(target=self.concrete_factory_create(),
                           pattern=other.concrete_factory_create()),
                Equivalent(target=self.abstract_product_type(),
                           pattern=other.abstract_product_type()),
            ])
        ])


class Decorator(DecoratorPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant([
                Equivalent(target=self.component(),
                           pattern=other.component()),
                Equivalent(target=self.concrete_component(),
                           pattern=other.concrete_component()),
                Equivalent(target=self.decorator(),
                           pattern=other.decorator()),
                Equivalent(target=self.concrete_decorator(),
                           pattern=other.concrete_decorator()),
                Equivalent(target=self.decorator_component(),
                           pattern=other.decorator_component()),
                Equivalent(target=self.decorator_end(),
                           pattern=other.decorator_end()),
                Equivalent(target=self.component_operation(),
                           pattern=other.component_operation()),
                Equivalent(target=self.decorator_operation(),
                           pattern=other.decorator_operation()),
                Equivalent(target=self.concrete_component_operation(),
                           pattern=other.concrete_component_operation()),
                Equivalent(target=self.concrete_component_operation(),
                           pattern=other.concrete_component_operation()),
                Equivalent(target=self.component_type(),
                           pattern=other.component_type()),
                Equivalent(target=self.decorator_type(),
                           pattern=other.decorator_type()),
            ])
        ])


class Burgers(object):
    INT_TYPE = Type(PrimitiveType('int'))

    @staticmethod
    def _price():
        return Operation(Burgers.INT_TYPE, 'price', Visibility.public,
                         is_static=False)

    @cached_method
    def cutlet_price(self):
        return self._price()

    @cached_method
    def cutlet(self):
        return Class('Cutlet', operations=[self.cutlet_price()])

    @cached_method
    def cutlet_type(self):
        return Type(self.cutlet())

    @cached_method
    def cheese_price(self):
        return self._price()

    @cached_method
    def cheese(self):
        return Class('Cheese', operations=[self.cheese_price()])

    @cached_method
    def cheese_type(self):
        return Type(self.cheese())

    @cached_method
    def burger_price(self):
        return self._price()

    @cached_method
    def burger(self):
        return Class('Burger', operations=[self.burger_price()])

    @cached_method
    def burger_type(self):
        return Type(self.burger())

    @cached_method
    def hamburger_cutlet(self):
        return Property(self.cutlet_type(), 'cutlet', Visibility.public,
                        is_static=False)

    @cached_method
    def hamburger_price(self):
        return self._price()

    @cached_method
    def hamburger(self):
        return Class('Hamburger', properties=[self.hamburger_cutlet()],
                     operations=[self.hamburger_price()])

    @cached_method
    def hamburger_type(self):
        return Type(self.hamburger())

    @cached_method
    def cheeseburger_cutlet(self):
        return Property(self.cutlet_type(), 'cutlet', Visibility.public,
                        is_static=False)

    @cached_method
    def cheeseburger_cheese(self):
        return Property(self.cheese_type(), 'cheese', Visibility.public,
                        is_static=False)

    @cached_method
    def cheeseburger_price(self):
        return self._price()

    @cached_method
    def cheeseburger(self):
        return Class('Cheeseburger', properties=[
            self.cheeseburger_cutlet(),
            self.cheeseburger_cheese(),
        ], operations=[self.cheeseburger_price()])

    @cached_method
    def cheeseburger_type(self):
        return Type(self.cheeseburger())

    @cached_method
    def burger_with_burger(self):
        return Property(self.burger_type(), 'burger', Visibility.public,
                        is_static=False)

    @cached_method
    def burger_with_price(self):
        return self._price()

    @cached_method
    def burger_with(self):
        return Class('BurgerWith', properties=[self.burger_with_burger()],
                     operations=[self.burger_with_price()])

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
        self.hamburger_cutlet().associations = [self.hamburger_end()]
        self.cheeseburger_cheese().associations = [self.cheeseburger_end()]
        self.cheeseburger_cutlet().associations = [self.cheeseburger_end()]
        self.burger_with_burger().associations = [self.burger_with_end()]
        self.cutlet().generals = [self.burger_with()]
        self.cheese().generals = [self.burger_with()]
        self.cheeseburger().generals = [self.burger()]
        self.hamburger().generals = [self.burger()]
        self.burger_with().generals = [self.burger()]
        return Diagram([
            self.burger(),
            self.burger_with(),
            self.hamburger(),
            self.cheeseburger(),
            self.cutlet(),
            self.cheese(),
        ])


class BukkitExample(object):
    def _create(self):
        return Operation(self.command_sender_type(), 'create',
                         Visibility.public, is_static=False)

    @cached_method
    def command_create(self):
        return self._create()

    @cached_method
    def command(self):
        return Class('Command', operations=[self.command_create()])

    @cached_method
    def command_sender(self):
        return Class('CommandSender')

    @cached_method
    def command_sender_type(self):
        return Type(self.command_sender())

    @cached_method
    def console_command_sender(self):
        return Class('ConsoleCommandSender')

    @cached_method
    def formatted_command_alias_create(self):
        return self._create()

    @cached_method
    def formatted_command_alias(self):
        return Class('FormattedCommandAlias', operations=[
            self.formatted_command_alias_create()
        ])

    @cached_method
    def plugin_command_create(self):
        return self._create()

    @cached_method
    def plugin_command(self):
        return Class('PluginCommand', operations=[self.plugin_command_create()])

    @cached_method
    def tab_completer(self):
        return Class('TabCompleter')

    @cached_method
    def diagram(self):
        self.console_command_sender().generals = [self.command_sender()]
        self.formatted_command_alias().generals = [self.command()]
        self.formatted_command_alias().suppliers = [self.command_sender()]
        self.plugin_command().generals = [self.command()]
        self.tab_completer().suppliers = [self.command_sender(), self.command()]
        return Diagram([
            self.console_command_sender(),
            self.plugin_command(),
            self.formatted_command_alias(),
            self.command(),
            self.command_sender(),
            self.tab_completer(),
        ])


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

    def test_match_decorator_pattern_in_burgers(self):
        t = Burgers()
        p = Decorator()
        expected_match_result = MatchResult([
            MatchVariant([
                Equivalent(t.burger(), p.component()),
                Equivalent(t.burger_with(), p.decorator()),
                Equivalent(t.cheese(), p.concrete_decorator()),
                Equivalent(t.cheeseburger(), p.concrete_component()),
                Equivalent(t.burger_with_end(), p.decorator_end()),
                Equivalent(t.burger_with_burger(), p.decorator_component()),
                Equivalent(t.burger_price(), p.component_operation()),
                Equivalent(t.burger_with_price(), p.decorator_operation()),
                Equivalent(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Equivalent(t.cheeseburger_price(),
                           p.concrete_component_operation()),
                Equivalent(t.burger_type(), p.component_type()),
                Equivalent(t.burger_with_type(), p.decorator_type()),
            ]),
            MatchVariant([
                Equivalent(t.burger(), p.component()),
                Equivalent(t.burger_with(), p.decorator()),
                Equivalent(t.cheese(), p.concrete_decorator()),
                Equivalent(t.hamburger(), p.concrete_component()),
                Equivalent(t.burger_with_end(), p.decorator_end()),
                Equivalent(t.burger_with_burger(), p.decorator_component()),
                Equivalent(t.burger_price(), p.component_operation()),
                Equivalent(t.burger_with_price(), p.decorator_operation()),
                Equivalent(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Equivalent(t.hamburger_price(),
                           p.concrete_component_operation()),
                Equivalent(t.burger_type(), p.component_type()),
                Equivalent(t.burger_with_type(), p.decorator_type()),
            ]),
            MatchVariant([
                Equivalent(t.burger(), p.component()),
                Equivalent(t.burger_with(), p.decorator()),
                Equivalent(t.cutlet(), p.concrete_decorator()),
                Equivalent(t.cheeseburger(), p.concrete_component()),
                Equivalent(t.burger_with_end(), p.decorator_end()),
                Equivalent(t.burger_with_burger(), p.decorator_component()),
                Equivalent(t.burger_price(), p.component_operation()),
                Equivalent(t.burger_with_price(), p.decorator_operation()),
                Equivalent(t.cutlet_price(),
                           p.concrete_decorator_operation()),
                Equivalent(t.cheeseburger_price(),
                           p.concrete_component_operation()),
                Equivalent(t.burger_type(), p.component_type()),
                Equivalent(t.burger_with_type(), p.decorator_type()),
            ]),
            MatchVariant([
                Equivalent(t.burger(), p.component()),
                Equivalent(t.burger_with(), p.decorator()),
                Equivalent(t.cutlet(), p.concrete_decorator()),
                Equivalent(t.hamburger(), p.concrete_component()),
                Equivalent(t.burger_with_end(), p.decorator_end()),
                Equivalent(t.burger_with_burger(), p.decorator_component()),
                Equivalent(t.burger_price(), p.component_operation()),
                Equivalent(t.burger_with_price(), p.decorator_operation()),
                Equivalent(t.cutlet_price(),
                           p.concrete_decorator_operation()),
                Equivalent(t.hamburger_price(),
                           p.concrete_component_operation()),
                Equivalent(t.burger_type(), p.component_type()),
                Equivalent(t.burger_with_type(), p.decorator_type()),
            ]),
        ])
        match_result = t.diagram().match(p.diagram())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_pattern_in_burgers_limit_one(self):
        t = Burgers()
        p = Decorator()
        expected_match_result = MatchResult([
            MatchVariant([
                Equivalent(t.burger(), p.component()),
                Equivalent(t.burger_with(), p.decorator()),
                Equivalent(t.cheese(), p.concrete_decorator()),
                Equivalent(t.hamburger(), p.concrete_component()),
                Equivalent(t.burger_with_end(), p.decorator_end()),
                Equivalent(t.burger_with_burger(), p.decorator_component()),
                Equivalent(t.burger_price(), p.component_operation()),
                Equivalent(t.burger_with_price(), p.decorator_operation()),
                Equivalent(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Equivalent(t.hamburger_price(),
                           p.concrete_component_operation()),
                Equivalent(t.burger_type(), p.component_type()),
                Equivalent(t.burger_with_type(), p.decorator_type()),
            ]),
        ])
        match_result = t.diagram().match(p.diagram(), 1)
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_abstract_factory_pattern_in_bukkit_example(self):
        t = BukkitExample()
        p = AbstractFactory()
        expected_match_result = MatchResult([
            MatchVariant([
                Equivalent(t.command(), p.abstract_factory()),
                Equivalent(t.command_sender(), p.abstract_product()),
                Equivalent(t.console_command_sender(), p.concrete_product()),
                Equivalent(t.plugin_command(), p.concrete_factory()),
                Equivalent(t.tab_completer(), p.client()),
                Equivalent(t.command_create(),
                           p.abstract_factory_create()),
                Equivalent(t.plugin_command_create(),
                           p.concrete_factory_create()),
                Equivalent(t.command_sender_type(), p.abstract_product_type())
            ]),
            MatchVariant([
                Equivalent(t.command(), p.abstract_factory()),
                Equivalent(t.command_sender(), p.abstract_product()),
                Equivalent(t.console_command_sender(), p.concrete_product()),
                Equivalent(t.formatted_command_alias(), p.concrete_factory()),
                Equivalent(t.tab_completer(), p.client()),
                Equivalent(t.command_create(),
                           p.abstract_factory_create()),
                Equivalent(t.formatted_command_alias_create(),
                           p.concrete_factory_create()),
                Equivalent(t.command_sender_type(), p.abstract_product_type())
            ]),
        ])
        match_result = t.diagram().match(p.diagram())
        assert_that(match_result, equal_to(expected_match_result))


class ReprDiagram(TestCase):
    def test_repr_empty_should_succeed(self):
        assert_that(repr(Diagram()), equal_to('Diagram()'))

    def test_repr_abstract_factory_empty_should_succeed(self):
        assert_that(repr(AbstractFactory().diagram()), equal_to(
            "Diagram((Class('Client'), Interface('AbstractFactory'), "
            "Interface('AbstractProduct'), Class('ConcreteFactory'), "
            "Class('ConcreteProduct')))"))

    def test_repr_decorator_empty_should_succeed(self):
        assert_that(repr(Decorator().diagram()), equal_to(
            "Diagram((Interface('Component'), Class('ConcreteComponent'), "
            "Interface('Decorator'), Class('ConcreteDecorator')))"))

if __name__ == '__main__':
    main()
