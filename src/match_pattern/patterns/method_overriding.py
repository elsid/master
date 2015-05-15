# coding: utf-8

from pattern_matcher import cached_method, Model, Class, Interface, Operation


class MethodOverriding(object):
    @cached_method
    def client(self):
        return Class('Client', operations=[self.client_invoke_operation()])

    @cached_method
    def interface(self):
        return Interface('Interface', operations=[self.interface_operation()])

    @cached_method
    def implementation(self):
        return Class('Implementation', generals=[self.interface()],
                     operations=[self.implementation_operation()])

    @cached_method
    def client_invoke_operation(self):
        return Operation(None, 'invoke_operation',
                         invocations=[self.interface_operation()])

    @cached_method
    def interface_operation(self):
        return self.operation()

    @cached_method
    def implementation_operation(self):
        return self.operation()

    @staticmethod
    def operation():
        return Operation(None, 'operation')

    @cached_method
    def create(self):
        return Model([self.client(), self.interface(), self.implementation()])


if __name__ == '__main__':
    print MethodOverriding().create()
