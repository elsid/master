# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Property,
    BinaryAssociation, Visibility)

from patterns.cached_method import cached_method


class Bridge(object):
    @cached_method
    def abstraction(self):
        return Class('Abstraction', [self.abstraction_implementor()],
                     [Operation(None, 'operation_impl', Visibility.public)])

    @cached_method
    def abstraction_type(self):
        return Type(self.abstraction())

    @cached_method
    def abstraction_implementor(self):
        return Property(self.implementor_type(), 'implementor')

    @cached_method
    def abstraction_end(self):
        return Property(self.abstraction_type(), 'Abstraction_end')

    @cached_method
    def implementor(self):
        return Interface('Implementor', [],
                         [Operation(None, 'operation_impl', Visibility.public)])

    @cached_method
    def implementor_type(self):
        return Type(self.implementor())

    @cached_method
    def concrete_implementor(self):
        return Class('ConcreteImplementor', operations=[
            Operation(None, 'operation_impl', Visibility.public),
        ])

    @cached_method
    def diagram(self):
        return Diagram(
            generalizations=[
                Generalization(derived=self.concrete_implementor(),
                               general=self.implementor()),
            ],
            associations=[
                BinaryAssociation({self.abstraction_implementor(),
                                   self.abstraction_end()}),
            ],
        )


if __name__ == '__main__':
    print Bridge().diagram()
