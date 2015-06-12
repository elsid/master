# coding: utf-8

from pattern_matcher import (
    Class, Type, Operation, Model, Interface, Property, Visibility,
    cached_method)


class Decorator(object):
    @cached_method
    def component(self):
        return Interface('Component', operations=[self.component_operation()])

    @cached_method
    def component_operation(self):
        return self._operation()

    @cached_method
    def component_type(self):
        return Type(self.component())

    @cached_method
    def concrete_component(self):
        return Class('ConcreteComponent', operations=[
            self.concrete_component_operation()
        ])

    @cached_method
    def concrete_component_operation(self):
        return self._operation()

    @cached_method
    def decorator_component(self):
        return Property('component', self.component_type(), is_static=False)

    @cached_method
    def decorator(self):
        return Class('Decorator', properties=[self.decorator_component()],
                     operations=[self.decorator_operation()])

    @cached_method
    def decorator_operation(self):
        return self._operation()

    @cached_method
    def decorator_type(self):
        return Type(self.decorator())

    @cached_method
    def concrete_decorator(self):
        return Class('ConcreteDecorator', operations=[
            self.concrete_decorator_operation()
        ])

    @cached_method
    def concrete_decorator_operation(self):
        return self._operation()

    @staticmethod
    def _operation():
        return Operation('operation', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def create(self):
        self.concrete_component().generals = [self.component()]
        self.decorator().generals = [self.component()]
        self.concrete_decorator().generals = [self.decorator()]
        self.decorator_operation().invocations = [self.component_operation()]
        return Model([
            self.component(),
            self.concrete_component(),
            self.decorator(),
            self.concrete_decorator(),
        ])


if __name__ == '__main__':
    print Decorator().create()
