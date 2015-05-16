# coding: utf-8

from pattern_matcher import (
    Class, Type, Operation, Model, Interface, Visibility, cached_method)


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
        return Operation('create', self.abstract_product_type(),
                         Visibility.PUBLIC, is_static=False)

    @cached_method
    def client(self):
        return Class('Client')

    @cached_method
    def create(self):
        self.concrete_factory().generals = [self.abstract_factory()]
        self.concrete_product().generals = [self.abstract_product()]
        self.client().suppliers = [self.abstract_factory(),
                                   self.abstract_product()]
        return Model([
            self.client(),
            self.abstract_factory(),
            self.abstract_product(),
            self.concrete_factory(),
            self.concrete_product(),
        ])


if __name__ == '__main__':
    print AbstractFactory().create()
