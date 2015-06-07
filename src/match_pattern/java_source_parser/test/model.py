# coding: utf-8

from os.path import dirname, join
from hamcrest import assert_that, equal_to, empty
from unittest import main
from pattern_matcher import (
    Model, Operation, Type, PrimitiveType, Interface, Class, Property,
    Visibility, cached_method)
from pattern_matcher.test.model import Burgers as BaseBurgers
from patterns import Decorator as BaseDecorator
from java_source_parser.model import make_model
from java_source_parser.errors import PlyjSyntaxError
from java_source_parser.test.classifiers import TestCaseWithParser
from java_source_parser.classifiers_members import PRIMITIVE_TYPES


class PrimitiveTypes(object):
    def __init__(self):

        def make_get_classifier(name):
            @cached_method
            def get_classifier(_):
                return PrimitiveType(name)

            return get_classifier

        def make_get_type(name):
            @cached_method
            def get_type(this):
                return Type(getattr(this, name)(this))

            return get_type

        for primitive in PRIMITIVE_TYPES:
            setattr(self, primitive, make_get_classifier(primitive))
            setattr(self, primitive + '_type', make_get_type(primitive))

    @cached_method
    def primitive_classifiers(self):
        return [getattr(self, x)(self) for x in PRIMITIVE_TYPES]

    @cached_method
    def create(self):
        return Model(self.primitive_classifiers())


class Decorator(BaseDecorator, PrimitiveTypes):
    VOID = Type(PrimitiveType('void'))

    @cached_method
    def component(self):
        return Interface('Component', operations=[
            Operation('operation', self.VOID, Visibility.PUBLIC,
                      is_static=False)
        ])

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', operations=[
            Operation('operation', self.VOID, Visibility.PUBLIC,
                      is_static=False),
        ])

    @cached_method
    def decorator_component(self):
        return Property(Type(self.component()), 'component', Visibility.PUBLIC,
                        is_static=False)

    @cached_method
    def decorator(self):
        return Interface('Decorator', properties=[
            self.decorator_component(),
        ], operations=[
            Operation('operation', self.VOID, Visibility.PUBLIC,
                      is_static=False),
        ])

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', operations=[
            Operation('operation', self.VOID, Visibility.PUBLIC,
                      is_static=False),
        ])

    @cached_method
    def create(self):
        base = super(Decorator, self).create()
        return Model(list(base.classifiers) + self.primitive_classifiers())


class Burgers(BaseBurgers, PrimitiveTypes):
    @cached_method
    def create(self):
        base = super(Burgers, self).create()
        return Model(list(base.classifiers) + self.primitive_classifiers())


class MakeModel(TestCaseWithParser):
    def test_from_empty_should_succeed(self):
        tree = self.parse('')
        model, errors = make_model(trees=[tree])
        assert_that(errors, empty())
        assert_that(model, equal_to(PrimitiveTypes().create()))

    def test_parse_with_syntax_errors_should_return_errors(self):
        file_path = join(dirname(__file__), 'java/syntax_errors.java')
        model, errors = make_model([file_path])
        assert_that(errors, equal_to([
            PlyjSyntaxError(file_path, "LexToken(NUM,'42',2,21)")]))
        assert_that(model, equal_to(Model()))

    def test_decorator_from_text_should_succeed(self):
        tree = self.parse('''
            interface Component {
                public void operation();
            }
            class ConcreteComponent implements Component {
                public void operation() {}
            }
            interface Decorator extends Component {
                public Component component = null;
                public void operation();
            }
            class ConcreteDecorator implements Decorator {
                public void operation() {}
            }
        ''')
        model, errors = make_model(trees=[tree])
        assert_that(errors, empty())
        assert_that(model, equal_to(Decorator().create()))

    def test_from_text_should_succeed(self):
        tree = self.parse('''
            interface Burger {
                public int price();
            }
            class BurgerWith implements Burger {
                public Burger burger;
                public int price() {}
            }
            class Cutlet extends BurgerWith {
                public int price() {}
            }
            class Cheese extends BurgerWith {
                public int price() {}
            }
            class Hamburger implements Burger {
                public Cutlet cutlet;
                public int price() {}
            }
            class Cheeseburger implements Burger {
                public Cutlet cutlet;
                public Cheese cheese;
                public int price() {}
            }
        ''')
        model, errors = make_model(trees=[tree])
        assert_that(errors, empty())
        assert_that(model, equal_to(Burgers().create()))

if __name__ == '__main__':
    main()
