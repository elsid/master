# coding: utf-8

from hamcrest import assert_that, equal_to, empty
from uml_matcher import (
    Diagram, Operation, Type, PrimitiveType, Aggregation, Interface, Class,
    Property, Generalization, BinaryAssociation)
from uml_matcher.diagram import eq_ignore_order
from uml_matcher.test.diagram import Factory, TargetDiagramFactory
from java_parser.diagram import make_diagram
from java_parser.test.classifiers import TestCaseWithParser


class DecoratorDiagramFactory(Factory):
    def __init__(self):
        void = Type(PrimitiveType('void'))

        def make_component(_):
            return Interface('Component', [], [Operation(void, 'operation')])

        def make_concrete_component(_):
            return Class('ConcreteComponent', [],
                         [Operation(void, 'operation')])

        def make_decorator_component(this):
            return Property(Type(this.component()), 'component')

        def make_decorator(this):
            return Interface('Decorator',
                             [this.decorator_component()],
                             [Operation(void, 'operation')])

        def make_concrete_decorator(_):
            return Class('ConcreteDecorator', [],
                         [Operation(void, 'operation')])

        def make_decorator_end(this):
            return Property(Type(this.decorator()), 'Decorator_end',
                            aggregation=Aggregation.none)

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


class BurgersDiagramFactory(Factory):
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
            return Property(this.burger_with_type(), 'BurgerWith_end')

        def make_hamburger_end(this):
            return Property(this.hamburger_type(), 'Hamburger_end')

        def make_cheeseburger_end(this):
            return Property(this.cheeseburger_type(), 'Cheeseburger_end')

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


class MakeDiagram(TestCaseWithParser):
    def test_make_from_empty_should_succeed(self):
        tree = self.parse('')
        diagram, errors = make_diagram(tree)
        assert_that(errors, empty())
        assert_that(diagram, equal_to(Diagram()))

    def test_make_decorator_from_text_should_succeed(self):
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
        diagram, errors = make_diagram(tree)
        assert_that(errors, empty())
        assert_that(diagram, equal_to(DecoratorDiagramFactory().diagram()))

    def test_make_from_text_should_succeed(self):
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
        diagram, errors = make_diagram(tree)
        assert_that(errors, empty())
        assert_that(diagram, equal_to(BurgersDiagramFactory().diagram()))
