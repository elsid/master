# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Property,
    BinaryAssociation, Visibility)

from patterns.cached_method import cached_method


class Bridge(object):
    @cached_method
    def abstraction(self):
        return Class('Abstraction', [self.abstraction_implementor()],
                     [Operation(None, 'operationImpl', Visibility.public)])

    @cached_method
    def abstraction_implementor(self):
        return Property(Type(self.implementor()), 'implementor')

    @cached_method
    def abstraction_end(self):
        return Property(Type(self.abstraction()), 'Abstraction_end')

    @cached_method
    def implementor(self):
        return Interface('Implementor', [],
                         [Operation(None, 'operationImpl', Visibility.public)])

    @cached_method
    def concrete_implementor(self):
        return Class('ConcreteImplementor', [],
                     [Operation(None, 'operationImpl', Visibility.public)])

    @cached_method
    def diagram(self):
        G = Generalization
        A = BinaryAssociation
        return Diagram(
            generalizations=[
                G(derived=self.concrete_implementor(), base=self.implementor()),
            ],
            associations=[
                A({self.abstraction_implementor(), self.abstraction_end()}),
            ],
        )


if __name__ == '__main__':
    print Bridge().diagram()
