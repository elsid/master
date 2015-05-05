# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Diagram, Interface, Visibility, cached_method)


class AbstractFactory(object):
    @cached_method
    def abstract_factory(self):
        return Interface('AbstractFactory', operations=[
            self.abstract_factory_create()
        ])

    @cached_method
    def abstract_factory_create(self):
        return self._create()

    @cached_method
    def concrete_factory(self):
        return Class('ConcreteFactory', operations=[
            self.concrete_factory_create()
        ])

    @cached_method
    def concrete_factory_create(self):
        return self._create()

    @cached_method
    def abstract_product(self):
        return Interface('AbstractProduct')

    @cached_method
    def abstract_product_type(self):
        return Type(self.abstract_product())

    @cached_method
    def concrete_product(self):
        return Class('ConcreteProduct')

    def _create(self):
        return Operation(self.abstract_product_type(), 'create',
                         Visibility.public, is_static=False)

    @cached_method
    def client(self):
        return Class('Client')

    @cached_method
    def diagram(self):
        self.concrete_factory().generals = [self.abstract_factory()]
        self.concrete_product().generals = [self.abstract_product()]
        self.client().suppliers = [self.abstract_factory(),
                                   self.abstract_product()]
        return Diagram([
            self.client(),
            self.abstract_factory(),
            self.abstract_product(),
            self.concrete_factory(),
            self.concrete_product(),
        ])


if __name__ == '__main__':
    print AbstractFactory().diagram()
