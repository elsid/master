# coding: utf-8

from os.path import dirname, join
from hamcrest import assert_that, equal_to, empty
from unittest import main
from uml_matcher import (
    Diagram, Operation, Type, PrimitiveType, Interface, Class, Property,
    Visibility, cached_method)
from uml_matcher.test.diagram import Burgers as BaseBurgers
from patterns import Decorator as BaseDecorator
from java_parser.diagram import make_diagram
from java_parser.errors import PlyjSyntaxError
from java_parser.test.classifiers import TestCaseWithParser
from java_parser.classifiers_members import PRIMITIVE_TYPES


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
    def diagram(self):
        return Diagram(self.primitive_classifiers())


class Decorator(BaseDecorator, PrimitiveTypes):
    VOID = Type(PrimitiveType('void'))

    @cached_method
    def component(self):
        return Interface('Component', operations=[
            Operation(self.VOID, 'operation', Visibility.public,
                      is_static=False)
        ])

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', operations=[
            Operation(self.VOID, 'operation', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def decorator_component(self):
        return Property(Type(self.component()), 'component', Visibility.public,
                        is_static=False)

    @cached_method
    def decorator(self):
        return Interface('Decorator', properties=[
            self.decorator_component(),
        ], operations=[
            Operation(self.VOID, 'operation', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', operations=[
            Operation(self.VOID, 'operation', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def diagram(self):
        base = super(Decorator, self).diagram()
        return Diagram(list(base.classifiers) + self.primitive_classifiers())


class Burgers(BaseBurgers, PrimitiveTypes):
    @cached_method
    def diagram(self):
        base = super(Burgers, self).diagram()
        return Diagram(list(base.classifiers) + self.primitive_classifiers())


class MakeDiagram(TestCaseWithParser):
    def test_from_empty_should_succeed(self):
        tree = self.parse('')
        diagram, errors = make_diagram(trees=[tree])
        assert_that(errors, empty())
        assert_that(diagram, equal_to(PrimitiveTypes().diagram()))

    def test_parse_with_syntax_errors_should_return_errors(self):
        file_path = join(dirname(__file__), 'java/syntax_errors.java')
        diagram, errors = make_diagram(files=[file_path])
        assert_that(errors, equal_to([
            PlyjSyntaxError(file_path, "LexToken(NUM,'42',2,21)")]))
        assert_that(diagram, equal_to(Diagram()))

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
        diagram, errors = make_diagram(trees=[tree])
        assert_that(errors, empty())
        assert_that(diagram, equal_to(Decorator().diagram()))

    def test_from_text_should_succeed(self):
        tree = self.parse('''
            class Burger {
                public int price() {}
            }
            class BurgerWith extends Burger {
                public Burger burger;
                public int price() {}
            }
            class Cutlet extends BurgerWith {
                public int price() {}
            }
            class Cheese extends BurgerWith {
                public int price() {}
            }
            class Hamburger extends Burger {
                public Cutlet cutlet;
                public int price() {}
            }
            class Cheeseburger extends Burger {
                public Cutlet cutlet;
                public Cheese cheese;
                public int price() {}
            }
        ''')
        diagram, errors = make_diagram(trees=[tree])
        assert_that(errors, empty())
        assert_that(diagram, equal_to(Burgers().diagram()))

if __name__ == '__main__':
    main()
