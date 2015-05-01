# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Property,
    BinaryAssociation, Visibility)

from patterns.cached_method import cached_method


class Decorator(object):
    @cached_method
    def component(self):
        return Interface('Component', [],
                         [Operation(None, 'operation', Visibility.public)])

    @cached_method
    def component_type(self):
        return Type(self.component())

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', [],
                     [Operation(None, 'operation', Visibility.public)])

    @cached_method
    def decorator_component(self):
        return Property(self.component_type(), 'component')

    @cached_method
    def decorator(self):
        return Interface('Decorator', [self.decorator_component()],
                         [Operation(None, 'operation', Visibility.public)])

    @cached_method
    def decorator_type(self):
        return Type(self.decorator())

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', [],
                     [Operation(None, 'operation', Visibility.public)])

    @cached_method
    def decorator_end(self):
        return Property(self.decorator_type(), 'Decorator_end')

    @cached_method
    def diagram(self):
        return Diagram(
            generalizations=[
                Generalization(derived=self.concrete_component(),
                               base=self.component()),
                Generalization(derived=self.decorator(),
                               base=self.component()),
                Generalization(derived=self.concrete_decorator(),
                               base=self.decorator()),
            ],
            associations=[
                BinaryAssociation({self.decorator_component(),
                                   self.decorator_end()}),
            ],
        )


if __name__ == '__main__':
    print Decorator().diagram()
