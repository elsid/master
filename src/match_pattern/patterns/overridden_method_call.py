#!/usr/bin/env python2
# coding: utf-8

from utils import cached_method
from pattern_matcher import Model, Class, Interface, Operation, Classifier


class OverriddenMethodCall(object):
    @cached_method
    def client(self):
        return Classifier('Client', operations=[self.client_invoke_operation()])

    @cached_method
    def interface(self):
        return Interface('Interface', operations=[self.interface_operation()])

    @cached_method
    def implementation(self):
        return Class('Implementation', generals=[self.interface()],
                     operations=[self.implementation_operation()])

    @cached_method
    def client_invoke_operation(self):
        return Operation('invoke_operation',
                         invocations=[self.interface_operation()])

    @cached_method
    def interface_operation(self):
        return self.operation()

    @cached_method
    def implementation_operation(self):
        return self.operation()

    @staticmethod
    def operation():
        return Operation('operation')

    @cached_method
    def create(self):
        return Model([self.client(), self.interface(), self.implementation()])


if __name__ == '__main__':
    print OverriddenMethodCall().create()
