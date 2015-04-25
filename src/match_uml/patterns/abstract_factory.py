# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Generalization, Diagram, Interface)

from patterns.cached_method import cached_method


class AbstractFactory(object):
    @cached_method
    def abstract_factory(self):
        return Interface('AbstractFactory', [], [self.product()])

    @cached_method
    def concrete_factory(self):
        return Class('ConcreteFactory', [], [self.product()])

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
        return Operation(self.abstract_product_type(), 'product')

    @cached_method
    def diagram(self):
        return Diagram(
            generalizations=[
                Generalization(base=self.abstract_factory(),
                               derived=self.concrete_factory()),
                Generalization(base=self.abstract_product(),
                               derived=self.concrete_product()),
            ],
        )


if __name__ == '__main__':
    print AbstractFactory().diagram()
