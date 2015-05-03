# coding: utf-8

from os.path import dirname, join
from hamcrest import assert_that, equal_to, empty
from unittest import main
from uml_matcher import (
    Diagram, Operation, Type, PrimitiveType, Interface, Class, Property,
    Generalization, BinaryAssociation, Visibility)
from patterns import cached_method
from java_parser.diagram import make_diagram
from java_parser.errors import PlyjSyntaxError
from java_parser.test.classifiers import TestCaseWithParser


class Decorator(object):
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
    def decorator_end(self):
        return Property(Type(self.decorator()), 'Decorator_end')

    @cached_method
    def diagram(self):
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


class Burgers(object):
    INT_TYPE = Type(PrimitiveType('int'))

    @cached_method
    def cutlet(self):
        return Class('Cutlet', operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def cutlet_type(self):
        return Type(self.cutlet())

    @cached_method
    def cheese(self):
        return Class('Cheese', operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def cheese_type(self):
        return Type(self.cheese())

    @cached_method
    def burger(self):
        return Class('Burger', operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False)
        ])

    @cached_method
    def burger_type(self):
        return Type(self.burger())

    @cached_method
    def hamburger_cutlet(self):
        return Property(self.cutlet_type(), 'cutlet', Visibility.public,
                        is_static=False)

    @cached_method
    def hamburger(self):
        return Class('Hamburger', properties=[self.hamburger_cutlet()],
                     operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False),
        ])

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
    def cheeseburger(self):
        return Class('Cheeseburger', properties=[
            self.cheeseburger_cutlet(),
            self.cheeseburger_cheese(),
        ], operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def cheeseburger_type(self):
        return Type(self.cheeseburger())

    @cached_method
    def burger_with_burger(self):
        return Property(self.burger_type(), 'burger', Visibility.public,
                        is_static=False)

    @cached_method
    def burger_with(self):
        return Class('BurgerWith', properties=[
            self.burger_with_burger(),
        ], operations=[
            Operation(self.INT_TYPE, 'price', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def burger_with_type(self):
        return Type(self.burger_with())

    @cached_method
    def burger_with_end(self):
        return Property(self.burger_with_type(), 'BurgerWith_end')

    @cached_method
    def hamburger_end(self):
        return Property(self.hamburger_type(), 'Hamburger_end')

    @cached_method
    def cheeseburger_end(self):
        return Property(self.cheeseburger_type(), 'Cheeseburger_end')

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


class MakeDiagram(TestCaseWithParser):
    def test_from_empty_should_succeed(self):
        tree = self.parse('')
        diagram, errors = make_diagram(trees=[tree])
        assert_that(errors, empty())
        assert_that(diagram, equal_to(Diagram()))

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
