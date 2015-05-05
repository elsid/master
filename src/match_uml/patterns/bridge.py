# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Diagram, Interface, Property, Visibility,
    cached_method)


class Bridge(object):
    @cached_method
    def abstraction(self):
        return Class('Abstraction', properties=[
            self.abstraction_implementor()
        ], operations=[
            Operation(None, 'operation_impl', Visibility.public,
                      is_static=False)
        ])

    @cached_method
    def abstraction_type(self):
        return Type(self.abstraction())

    @cached_method
    def abstraction_implementor(self):
        return Property(self.implementor_type(), 'implementor', is_static=False)

    @cached_method
    def abstraction_end(self):
        return Property(self.abstraction_type(), 'Abstraction_end')

    @cached_method
    def implementor(self):
        return Interface('Implementor', operations=[
            Operation(None, 'operation_impl', Visibility.public,
                      is_static=False)
        ])

    @cached_method
    def implementor_type(self):
        return Type(self.implementor())

    @cached_method
    def concrete_implementor(self):
        return Class('ConcreteImplementor', operations=[
            Operation(None, 'operation_impl', Visibility.public,
                      is_static=False),
        ])

    @cached_method
    def diagram(self):
        self.concrete_implementor().generals = [self.implementor()]
        self.abstraction_implementor().associations = [self.abstraction_end()]
        return Diagram([
            self.abstraction(),
            self.implementor(),
            self.concrete_implementor(),
        ])


if __name__ == '__main__':
    print Bridge().diagram()
