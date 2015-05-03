# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface, Visibility,
    Dependency)

from patterns.cached_method import cached_method


class AbstractFactory(object):
    @cached_method
    def abstract_factory(self):
        return Interface('AbstractFactory', operations=[self.product()])

    @cached_method
    def concrete_factory(self):
        return Class('ConcreteFactory', operations=[self.product()])

    @cached_method
    def abstract_product(self):
        return Interface('AbstractProduct')

    @cached_method
    def abstract_product_type(self):
        return Type(self.abstract_product())

    @cached_method
    def concrete_product(self):
        return Class('ConcreteProduct')

    @cached_method
    def product(self):
        return Operation(self.abstract_product_type(), 'product',
                         Visibility.public)

    @cached_method
    def client(self):
        return Class('Client')

    @cached_method
    def diagram(self):
        return Diagram(
            generalizations=[
                Generalization(general=self.abstract_factory(),
                               derived=self.concrete_factory()),
                Generalization(general=self.abstract_product(),
                               derived=self.concrete_product()),
            ],
            dependencies=[
                Dependency(client=self.client(),
                           supplier=self.abstract_factory()),
                Dependency(client=self.client(),
                           supplier=self.abstract_product()),
            ],
        )


if __name__ == '__main__':
    print AbstractFactory().diagram()
