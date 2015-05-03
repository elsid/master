# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Diagram, Interface, Property, Visibility)

from patterns.cached_method import cached_method


class Decorator(object):
    @cached_method
    def component(self):
        return Interface('Component', operations=[
            Operation(None, 'operation', Visibility.public, is_static=False)
        ])

    @cached_method
    def component_type(self):
        return Type(self.component())

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', operations=[
            Operation(None, 'operation', Visibility.public, is_static=False),
        ])

    @cached_method
    def decorator_component(self):
        return Property(self.component_type(), 'component', is_static=False)

    @cached_method
    def decorator(self):
        return Interface('Decorator', properties=[
            self.decorator_component(),
        ], operations=[
            Operation(None, 'operation', Visibility.public, is_static=False),
        ])

    @cached_method
    def decorator_type(self):
        return Type(self.decorator())

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', operations=[
            Operation(None, 'operation', Visibility.public, is_static=False),
        ])

    @cached_method
    def decorator_end(self):
        return Property(self.decorator_type(), 'Decorator_end')

    @cached_method
    def diagram(self):
        self.concrete_component().generals = [self.component()]
        self.decorator().generals = [self.component()]
        self.concrete_decorator().generals = [self.decorator()]
        self.decorator_component().associations = [self.decorator_end()]
        return Diagram([
            self.component(),
            self.concrete_component(),
            self.decorator(),
            self.concrete_decorator(),
        ])


if __name__ == '__main__':
    print Decorator().diagram()
