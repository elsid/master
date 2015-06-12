# coding: utf-8

from pattern_matcher import (
    Class, Type, Operation, Model, Interface, Property, Visibility, Classifier,
    cached_method)


class Adapter(object):
    @cached_method
    def adapter(self):
        return Interface('Adapter', operations=[self.adapter_operation()])

    @cached_method
    def concrete_adapter(self):
        return Class('ConcreteAdapter', properties=[
            self.concrete_adapter_adaptee()
        ], operations=[
            self.concrete_adapter_operation()
        ])

    @cached_method
    def adaptee(self):
        return Classifier('Adaptee', operations=[
            self.adaptee_adapted_operation()
        ])

    @cached_method
    def adaptee_type(self):
        return Type(self.adaptee())

    @cached_method
    def adapter_operation(self):
        return Operation('operation', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def concrete_adapter_adaptee(self):
        return Property('adaptee', self.adaptee_type(), Visibility.PRIVATE,
                        is_static=False)

    @cached_method
    def concrete_adapter_operation(self):
        return Operation('operation', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def adaptee_adapted_operation(self):
        return Operation('adapted_operation', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def create(self):
        self.concrete_adapter().generals = [self.adapter()]
        self.concrete_adapter_operation().invocations = [
            self.adaptee_adapted_operation()]
        return Model([
            self.adapter(),
            self.concrete_adapter(),
            self.adaptee(),
        ])


if __name__ == '__main__':
    print Adapter().create()
