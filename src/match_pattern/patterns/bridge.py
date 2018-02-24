#!/usr/bin/env python2
# coding: utf-8

from utils import cached_method
from pattern_matcher import (
    Class, Type, Operation, Model, Interface, Property, Visibility)


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
        return Property('implementor', self.implementor_type(), is_static=False)

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
        return Operation('operation', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def implementor_operation_impl(self):
        return Operation('operation_impl', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def concrete_implementor_operation_impl(self):
        return Operation('operation_impl', visibility=Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def create(self):
        self.concrete_implementor().generals = [self.implementor()]
        self.abstraction_operation().invocations = [
            self.implementor_operation_impl()]
        return Model([
            self.abstraction(),
            self.implementor(),
            self.concrete_implementor(),
        ])


if __name__ == '__main__':
    print Bridge().create()
