# coding: utf-8

from pattern_matcher import (
    Class, Type, Operation, Model, Interface, Visibility, Parameter, Direction,
    cached_method)


class Visitor(object):
    @cached_method
    def client(self):
        return Class('Client')

    @cached_method
    def element(self):
        return Class('Element', operations=[self.element_accept()])

    @cached_method
    def concrete_element(self):
        return Class('ConcreteElement', operations=[
            self.concrete_element_accept(),
        ])

    @cached_method
    def visitor(self):
        return Interface('Visitor', operations=[self.visitor_visit()])

    @cached_method
    def concrete_visitor(self):
        return Class('ConcreteVisitor', operations=[
            self.concrete_visitor_visit(),
        ])

    @cached_method
    def visitor_type(self):
        return Type(self.visitor())

    @cached_method
    def concrete_element_type(self):
        return Type(self.concrete_element())

    @cached_method
    def visitor_visit(self):
        return self._visit()

    @cached_method
    def concrete_visitor_visit(self):
        return self._visit()

    @cached_method
    def element_accept(self):
        return self._accept()

    @cached_method
    def concrete_element_accept(self):
        return self._accept()

    def _visit(self):
        return Operation('visit', visibility=Visibility.PUBLIC)

    def _accept(self):
        return Operation('accept', visibility=Visibility.PUBLIC)

    @cached_method
    def visitor_visit_concrete_element(self):
        return self._visit_concrete_element()

    @cached_method
    def concrete_visitor_visit_concrete_element(self):
        return self._visit_concrete_element()

    @cached_method
    def element_accept_visitor(self):
        return self._accept_visitor()

    @cached_method
    def concrete_element_accept_visitor(self):
        return self._accept_visitor()

    def _visit_concrete_element(self):
        return Parameter('concrete_element', self.concrete_element_type(),
                         Direction.IN)

    def _accept_visitor(self):
        return Parameter('visitor', self.visitor_type(), Direction.IN)

    @cached_method
    def create(self):
        self.client().suppliers = [self.element(), self.visitor()]
        self.concrete_element().generals = [self.element()]
        self.concrete_visitor().generals = [self.visitor()]
        self.concrete_element_accept().invocations = [self.visitor_visit()]
        self.visitor_visit().parameters = [
            self.visitor_visit_concrete_element()]
        self.concrete_visitor_visit().parameters = [
            self.concrete_visitor_visit_concrete_element()]
        self.element_accept().parameters = [self.element_accept_visitor()]
        self.concrete_element_accept().parameters = [
            self.concrete_element_accept_visitor()]
        return Model([
            self.client(),
            self.concrete_element(),
            self.concrete_visitor(),
            self.element(),
            self.visitor(),
        ])


if __name__ == '__main__':
    print Visitor().create()
