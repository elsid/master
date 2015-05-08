# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Diagram, Interface, Property, Visibility,
    cached_method)


class Bridge(object):
    @cached_method
    def abstraction(self):
        return Class('Abstraction', properties=[self.abstraction_implementor()],
                     operations=[self.abstraction_operation()])

    @cached_method
    def abstraction_type(self):
        return Type(self.abstraction())

    @cached_method
    def abstraction_implementor(self):
        return Property(self.implementor_type(), 'implementor', is_static=False)

    @cached_method
    def implementor(self):
        return Interface('Implementor',
                         operations=[self.implementor_operation_impl()])

    @cached_method
    def implementor_type(self):
        return Type(self.implementor())

    @cached_method
    def concrete_implementor(self):
        return Class('ConcreteImplementor',
                     operations=[self.concrete_implementor_operation_impl()])

    @cached_method
    def abstraction_operation(self):
        return Operation(None, 'operation', Visibility.public,
                         is_static=False)

    @cached_method
    def implementor_operation_impl(self):
        return Operation(None, 'operation_impl', Visibility.public,
                         is_static=False)

    @cached_method
    def concrete_implementor_operation_impl(self):
        return Operation(None, 'operation_impl', Visibility.public,
                         is_static=False)

    @cached_method
    def diagram(self):
        self.concrete_implementor().generals = [self.implementor()]
        return Diagram([
            self.abstraction(),
            self.implementor(),
            self.concrete_implementor(),
        ])


if __name__ == '__main__':
    print Bridge().diagram()
