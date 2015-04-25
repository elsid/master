# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Property,
    Aggregation, BinaryAssociation)

from patterns.cached_method import cached_method


class Decorator(object):
    @cached_method
    def component(self):
        return Interface('Component', [], [Operation(None, 'operation')])

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', [], [Operation(None, 'operation')])

    @cached_method
    def decorator_component(self):
        return Property(Type(self.component()), 'component')

    @cached_method
    def decorator(self):
        return Interface('Decorator', [self.decorator_component()],
                         [Operation(None, 'operation')])

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', [], [Operation(None, 'operation')])

    @cached_method
    def decorator_end(self):
        return Property(Type(self.decorator()), 'Decorator_end',
                        aggregation=Aggregation.shared)

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


if __name__ == '__main__':
    print Decorator().diagram()
