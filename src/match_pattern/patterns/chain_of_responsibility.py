# coding: utf-8

from pattern_matcher import (
    Class, Type, Operation, Model, Visibility, Property, Interface,
    cached_method)


class ChainOfResponsibility(object):
    @cached_method
    def client(self):
        return Class('Client')

    @cached_method
    def handler(self):
        return Interface('Handler', operations=[self.handler_handle_request()])

    @cached_method
    def concrete_handler(self):
        return Class('ConcreteHandler',
                     operations=[self.handler_handle_request()])

    @cached_method
    def handler_next(self):
        return Property(self.handler_type(), 'next', is_static=False)

    @cached_method
    def handler_handle_request(self):
        return self.handle_request()

    @cached_method
    def concrete_handler_handle_request(self):
        return self.handle_request()

    @cached_method
    def handler_type(self):
        return Type(self.handler())

    @staticmethod
    def handle_request():
        return Operation(None, 'handle_request', Visibility.PUBLIC,
                         is_static=False)

    @cached_method
    def create(self):
        self.client().suppliers = [self.handler()]
        self.concrete_handler().generals = [self.handler()]
        self.handler().properties = [self.handler_next()]
        return Model([
            self.client(),
            self.handler(),
            self.concrete_handler(),
        ])


if __name__ == '__main__':
    print ChainOfResponsibility().create()
