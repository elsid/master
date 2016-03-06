# coding: utf-8

import yaml
from os.path import dirname, join
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from graph_matcher import Isomorphic
from utils import cached_method
from patterns import (
    AbstractFactory as AbstractFactoryPattern,
    Decorator as DecoratorPattern,
    Memento as MementoPattern,
    Visitor as VisitorPattern,
)
from pattern_matcher.operation import Operation
from pattern_matcher.property import Property
from pattern_matcher.type import Type
from pattern_matcher.primitive_type import PrimitiveType
from pattern_matcher.model import Model
from pattern_matcher.match import MatchResult, MatchVariant
from pattern_matcher.visibility import Visibility
from pattern_matcher.interface import Interface
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class


class AbstractFactory(AbstractFactoryPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant([
                Isomorphic(target=self.abstract_factory(),
                           pattern=other.abstract_factory()),
                Isomorphic(target=self.concrete_factory(),
                           pattern=other.concrete_factory()),
                Isomorphic(target=self.abstract_product(),
                           pattern=other.abstract_product()),
                Isomorphic(target=self.concrete_product(),
                           pattern=other.concrete_product()),
                Isomorphic(target=self.abstract_factory_create(),
                           pattern=other.abstract_factory_create()),
                Isomorphic(target=self.concrete_factory_create(),
                           pattern=other.concrete_factory_create()),
                Isomorphic(target=self.abstract_product_type(),
                           pattern=other.abstract_product_type()),
            ])
        ])


class Decorator(DecoratorPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant([
                Isomorphic(target=self.component(),
                           pattern=other.component()),
                Isomorphic(target=self.concrete_component(),
                           pattern=other.concrete_component()),
                Isomorphic(target=self.decorator(),
                           pattern=other.decorator()),
                Isomorphic(target=self.concrete_decorator(),
                           pattern=other.concrete_decorator()),
                Isomorphic(target=self.decorator_component(),
                           pattern=other.decorator_component()),
                Isomorphic(target=self.component_operation(),
                           pattern=other.component_operation()),
                Isomorphic(target=self.decorator_operation(),
                           pattern=other.decorator_operation()),
                Isomorphic(target=self.concrete_component_operation(),
                           pattern=other.concrete_component_operation()),
                Isomorphic(target=self.concrete_component_operation(),
                           pattern=other.concrete_component_operation()),
                Isomorphic(target=self.component_type(),
                           pattern=other.component_type()),
            ])
        ])


class Visitor(VisitorPattern):
    def match_result(self, other):
        return MatchResult([
            MatchVariant([
                Isomorphic(target=self.concrete_element(),
                           pattern=other.concrete_element()),
                Isomorphic(target=self.concrete_visitor(),
                           pattern=other.concrete_visitor()),
                Isomorphic(target=self.element(), pattern=other.element()),
                Isomorphic(target=self.visitor(), pattern=other.visitor()),
                Isomorphic(target=self.visitor_visit(),
                           pattern=other.visitor_visit()),
                Isomorphic(target=self.concrete_visitor_visit(),
                           pattern=other.concrete_visitor_visit()),
                Isomorphic(target=self.element_accept(),
                           pattern=other.element_accept()),
                Isomorphic(target=self.concrete_element_accept(),
                           pattern=other.concrete_element_accept()),
                Isomorphic(target=self.visitor_type(),
                           pattern=other.visitor_type()),
                Isomorphic(target=self.concrete_element_type(),
                           pattern=other.concrete_element_type()),
                Isomorphic(target=self.visitor_visit_concrete_element(),
                           pattern=other.visitor_visit_concrete_element()),
                Isomorphic(
                    target=self.concrete_visitor_visit_concrete_element(),
                    pattern=other.concrete_visitor_visit_concrete_element(),
                ),
                Isomorphic(target=self.element_accept_visitor(),
                           pattern=other.element_accept_visitor()),
                Isomorphic(target=self.concrete_element_accept_visitor(),
                           pattern=other.concrete_element_accept_visitor()),
            ])
        ])


class Burgers(object):
    INT_TYPE = Type(PrimitiveType('int'))

    @staticmethod
    def _price():
        return Operation('price', Burgers.INT_TYPE, Visibility.PUBLIC,
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
        return Interface('Burger', operations=[self.burger_price()])

    @cached_method
    def burger_type(self):
        return Type(self.burger())

    @cached_method
    def hamburger_cutlet(self):
        return Property('cutlet', self.cutlet_type(), Visibility.PUBLIC,
                        is_static=False)

    @cached_method
    def hamburger_price(self):
        return self._price()

    @cached_method
    def hamburger(self):
        return Class('Hamburger', properties=[self.hamburger_cutlet()],
                     operations=[self.hamburger_price()])

    @cached_method
    def cheeseburger_cutlet(self):
        return Property('cutlet', self.cutlet_type(), Visibility.PUBLIC,
                        is_static=False)

    @cached_method
    def cheeseburger_cheese(self):
        return Property('cheese', self.cheese_type(), Visibility.PUBLIC,
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
    def burger_with_burger(self):
        return Property('burger', self.burger_type(), Visibility.PUBLIC,
                        is_static=False)

    @cached_method
    def burger_with_price(self):
        return self._price()

    @cached_method
    def burger_with(self):
        return Class('BurgerWith', properties=[self.burger_with_burger()],
                     operations=[self.burger_with_price()])

    @cached_method
    def create(self):
        self.cutlet().generals = [self.burger_with()]
        self.cheese().generals = [self.burger_with()]
        self.cheeseburger().generals = [self.burger()]
        self.hamburger().generals = [self.burger()]
        self.burger_with().generals = [self.burger()]
        self.burger_with_price().invocations = [self.burger_price()]
        return Model([
            self.burger(),
            self.burger_with(),
            self.hamburger(),
            self.cheeseburger(),
            self.cutlet(),
            self.cheese(),
        ])


class BukkitExample(object):
    def _create(self):
        return Operation('create', self.command_sender_type(),
                         Visibility.PUBLIC, is_static=False)

    @cached_method
    def command_create(self):
        return self._create()

    @cached_method
    def command(self):
        return Interface('Command', operations=[self.command_create()])

    @cached_method
    def command_sender(self):
        return Interface('CommandSender')

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
    def create(self):
        self.console_command_sender().generals = [self.command_sender()]
        self.formatted_command_alias().generals = [self.command()]
        self.formatted_command_alias().suppliers = [self.command_sender()]
        self.plugin_command().generals = [self.command()]
        self.tab_completer().suppliers = [self.command_sender(), self.command()]
        self.plugin_command().suppliers = [self.console_command_sender()]
        self.formatted_command_alias().suppliers = [
            self.console_command_sender()]
        return Model([
            self.console_command_sender(),
            self.plugin_command(),
            self.formatted_command_alias(),
            self.command(),
            self.command_sender(),
            self.tab_completer(),
        ])


class MatchModel(TestCase):
    def test_match_empty_should_has_empty_match_result(self):
        assert_that(Model().match(Model()), equal_to(MatchResult()))

    def test_match_abstract_factory_patterns(self):
        target = AbstractFactory()
        pattern = AbstractFactory()
        expected_match_result = target.match_result(pattern)
        match_result = target.create().match(pattern.create())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_patterns(self):
        target = Decorator()
        pattern = Decorator()
        expected_match_result = target.match_result(pattern)
        match_result = target.create().match(pattern.create())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_visitor_patterns(self):
        target = Visitor()
        pattern = Visitor()
        assert_that(target.create(), equal_to(pattern.create()))
        expected_match_result = target.match_result(pattern)
        match_result = target.create().match(pattern.create())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_pattern_in_burgers(self):
        t = Burgers()
        p = Decorator()
        expected_match_result = MatchResult([
            MatchVariant([
                Isomorphic(t.burger(), p.component()),
                Isomorphic(t.burger_with(), p.decorator()),
                Isomorphic(t.cheese(), p.concrete_decorator()),
                Isomorphic(t.cheeseburger(), p.concrete_component()),
                Isomorphic(t.burger_with_burger(), p.decorator_component()),
                Isomorphic(t.burger_price(), p.component_operation()),
                Isomorphic(t.burger_with_price(), p.decorator_operation()),
                Isomorphic(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Isomorphic(t.cheeseburger_price(),
                           p.concrete_component_operation()),
                Isomorphic(t.burger_type(), p.component_type()),
            ]),
            MatchVariant([
                Isomorphic(t.burger(), p.component()),
                Isomorphic(t.burger_with(), p.decorator()),
                Isomorphic(t.cheese(), p.concrete_decorator()),
                Isomorphic(t.hamburger(), p.concrete_component()),
                Isomorphic(t.burger_with_burger(), p.decorator_component()),
                Isomorphic(t.burger_price(), p.component_operation()),
                Isomorphic(t.burger_with_price(), p.decorator_operation()),
                Isomorphic(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Isomorphic(t.hamburger_price(),
                           p.concrete_component_operation()),
                Isomorphic(t.burger_type(), p.component_type()),
            ]),
            MatchVariant([
                Isomorphic(t.burger(), p.component()),
                Isomorphic(t.burger_with(), p.decorator()),
                Isomorphic(t.cutlet(), p.concrete_decorator()),
                Isomorphic(t.cheeseburger(), p.concrete_component()),
                Isomorphic(t.burger_with_burger(), p.decorator_component()),
                Isomorphic(t.burger_price(), p.component_operation()),
                Isomorphic(t.burger_with_price(), p.decorator_operation()),
                Isomorphic(t.cutlet_price(),
                           p.concrete_decorator_operation()),
                Isomorphic(t.cheeseburger_price(),
                           p.concrete_component_operation()),
                Isomorphic(t.burger_type(), p.component_type()),
            ]),
            MatchVariant([
                Isomorphic(t.burger(), p.component()),
                Isomorphic(t.burger_with(), p.decorator()),
                Isomorphic(t.cutlet(), p.concrete_decorator()),
                Isomorphic(t.hamburger(), p.concrete_component()),
                Isomorphic(t.burger_with_burger(), p.decorator_component()),
                Isomorphic(t.burger_price(), p.component_operation()),
                Isomorphic(t.burger_with_price(), p.decorator_operation()),
                Isomorphic(t.cutlet_price(),
                           p.concrete_decorator_operation()),
                Isomorphic(t.hamburger_price(),
                           p.concrete_component_operation()),
                Isomorphic(t.burger_type(), p.component_type()),
            ]),
        ])
        assert_that(t.burger().equiv_pattern(p.component()))
        assert_that(t.burger_price().equiv_pattern(p.component_operation()))
        assert_that(t.burger_type().equiv_pattern(p.component_type()))
        assert_that(t.burger_with().equiv_pattern(p.decorator()))
        assert_that(t.burger_with_burger().equiv_pattern(
            p.decorator_component()))
        assert_that(t.burger_with_price().equiv_pattern(
            p.decorator_operation()))
        assert_that(t.cheese().equiv_pattern(p.concrete_decorator()))
        assert_that(t.cheese_price().equiv_pattern(
            p.concrete_decorator_operation()))
        assert_that(t.cheeseburger().equiv_pattern(p.concrete_component()))
        assert_that(t.cheeseburger_price().equiv_pattern(
            p.concrete_component_operation()))
        assert_that(t.cutlet().equiv_pattern(p.concrete_decorator()))
        assert_that(t.cutlet_price().equiv_pattern(
            p.concrete_decorator_operation()))
        assert_that(t.hamburger().equiv_pattern(p.concrete_component()))
        assert_that(t.hamburger_price().equiv_pattern(
            p.concrete_component_operation()))
        match_result = t.create().match(p.create())
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_decorator_pattern_in_burgers_limit_one(self):
        t = Burgers()
        p = Decorator()
        expected_match_result = MatchResult([
            MatchVariant([
                Isomorphic(t.burger(), p.component()),
                Isomorphic(t.burger_with(), p.decorator()),
                Isomorphic(t.cheese(), p.concrete_decorator()),
                Isomorphic(t.cheeseburger(), p.concrete_component()),
                Isomorphic(t.burger_with_burger(), p.decorator_component()),
                Isomorphic(t.burger_price(), p.component_operation()),
                Isomorphic(t.burger_with_price(), p.decorator_operation()),
                Isomorphic(t.cheese_price(),
                           p.concrete_decorator_operation()),
                Isomorphic(t.cheeseburger_price(),
                           p.concrete_component_operation()),
                Isomorphic(t.burger_type(), p.component_type()),
            ]),
        ])
        match_result = t.create().match(p.create(), 1)
        assert_that(match_result, equal_to(expected_match_result))

    def test_match_abstract_factory_pattern_in_bukkit_example(self):
        t = BukkitExample()
        p = AbstractFactory()
        expected_match_result = MatchResult([
            MatchVariant([
                Isomorphic(t.command(), p.abstract_factory()),
                Isomorphic(t.command_sender(), p.abstract_product()),
                Isomorphic(t.console_command_sender(), p.concrete_product()),
                Isomorphic(t.plugin_command(), p.concrete_factory()),
                Isomorphic(t.command_create(),
                           p.abstract_factory_create()),
                Isomorphic(t.plugin_command_create(),
                           p.concrete_factory_create()),
                Isomorphic(t.command_sender_type(), p.abstract_product_type())
            ]),
            MatchVariant([
                Isomorphic(t.command(), p.abstract_factory()),
                Isomorphic(t.command_sender(), p.abstract_product()),
                Isomorphic(t.console_command_sender(), p.concrete_product()),
                Isomorphic(t.formatted_command_alias(), p.concrete_factory()),
                Isomorphic(t.command_create(),
                           p.abstract_factory_create()),
                Isomorphic(t.formatted_command_alias_create(),
                           p.concrete_factory_create()),
                Isomorphic(t.command_sender_type(), p.abstract_product_type())
            ]),
        ])
        assert_that(t.command().equiv_pattern(p.abstract_factory()))
        assert_that(t.command_create().equiv_pattern(
            p.abstract_factory_create()))
        assert_that(t.command_sender().equiv_pattern(p.abstract_product()))
        assert_that(t.command_sender_type().equiv_pattern(
            p.abstract_product_type()))
        assert_that(t.console_command_sender().equiv_pattern(
            p.concrete_product()))
        assert_that(t.formatted_command_alias().equiv_pattern(
            p.concrete_factory()))
        assert_that(t.formatted_command_alias_create().equiv_pattern(
            p.concrete_factory_create()))
        assert_that(t.plugin_command().equiv_pattern(p.concrete_factory()))
        assert_that(t.plugin_command_create().equiv_pattern(
            p.concrete_factory_create()))
        match_result = t.create().match(p.create())
        assert_that(match_result, equal_to(expected_match_result))


class ReprModel(TestCase):
    def test_repr_empty_should_succeed(self):
        assert_that(repr(Model()), equal_to('Model()'))

    def test_repr_abstract_factory_empty_should_succeed(self):
        assert_that(repr(AbstractFactory().create()), equal_to(
            "Model((Interface('AbstractFactory'), "
            "Interface('AbstractProduct'), Class('ConcreteFactory'), "
            "Class('ConcreteProduct')))"))

    def test_repr_decorator_empty_should_succeed(self):
        assert_that(repr(Decorator().create()), equal_to(
            "Model((Interface('Component'), Class('ConcreteComponent'), "
            "Class('Decorator'), Class('ConcreteDecorator')))"))


class YamlModel(TestCase):
    def test_yaml_dump(self):
        assert_that(yaml.dump(Model()), equal_to("!Model []\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Model []\n"), equal_to(Model()))

    def test_yaml_dump_abstract_factory_pattern(self):
        model = AbstractFactoryPattern().create()
        file_path = join(dirname(__file__), 'data/abstract_factory.yaml')
        assert_that(yaml.dump(model, default_flow_style=False),
                    equal_to(open(file_path).read()))

    def test_yaml_load_abstract_factory_pattern(self):
        model = AbstractFactoryPattern().create()
        file_path = join(dirname(__file__), 'data/abstract_factory.yaml')
        assert_that(yaml.load(open(file_path)), equal_to(model))

    def test_yaml_dump_decorator_pattern(self):
        model = DecoratorPattern().create()
        file_path = join(dirname(__file__), 'data/decorator.yaml')
        assert_that(yaml.dump(model, default_flow_style=False),
                    equal_to(open(file_path).read()))

    def test_yaml_load_decorator_pattern(self):
        model = DecoratorPattern().create()
        file_path = join(dirname(__file__), 'data/decorator.yaml')
        assert_that(yaml.load(open(file_path)), equal_to(model))

    def test_yaml_dump_memento_pattern(self):
        model = MementoPattern().create()
        file_path = join(dirname(__file__), 'data/memento.yaml')
        assert_that(yaml.dump(model, default_flow_style=False),
                    equal_to(open(file_path).read()))

    def test_yaml_load_memento_pattern(self):
        model = MementoPattern().create()
        file_path = join(dirname(__file__), 'data/memento.yaml')
        assert_that(yaml.load(open(file_path)), equal_to(model))

    def test_yaml_dump_burgers(self):
        model = Burgers().create()
        file_path = join(dirname(__file__), 'data/burgers.yaml')
        assert_that(yaml.dump(model, default_flow_style=False),
                    equal_to(open(file_path).read()))

    def test_yaml_load_burgers(self):
        model = Burgers().create()
        file_path = join(dirname(__file__), 'data/burgers.yaml')
        assert_that(yaml.load(open(file_path)), equal_to(model))
