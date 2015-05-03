# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Property,
    BinaryAssociation, Visibility)

from patterns.cached_method import cached_method


class Decorator(object):
    @cached_method
    def component(self):
        return Interface('Component', operations=[
            Operation(None, 'operation', Visibility.public)
        ])

    @cached_method
    def component_type(self):
        return Type(self.component())

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', operations=[
            Operation(None, 'operation', Visibility.public),
        ])

    @cached_method
    def decorator_component(self):
        return Property(self.component_type(), 'component')

    @cached_method
    def decorator(self):
        return Interface('Decorator', properties=[
            self.decorator_component(),
        ], operations=[
            Operation(None, 'operation', Visibility.public),
        ])

    @cached_method
    def decorator_type(self):
        return Type(self.decorator())

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', operations=[
            Operation(None, 'operation', Visibility.public),
        ])

    @cached_method
    def decorator_end(self):
        return Property(self.decorator_type(), 'Decorator_end')

    @cached_method
    def diagram(self):
        return Diagram(
            generalizations=[
                Generalization(derived=self.concrete_component(),
                               general=self.component()),
                Generalization(derived=self.decorator(),
                               general=self.component()),
                Generalization(derived=self.concrete_decorator(),
                               general=self.decorator()),
            ],
            associations=[
                BinaryAssociation({self.decorator_component(),
                                   self.decorator_end()}),
            ],
        )


if __name__ == '__main__':
    print Decorator().diagram()
