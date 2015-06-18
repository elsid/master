# coding: utf-8

from utils import cached_method
from pattern_matcher import (
    Class, Type, Operation, Model, Visibility, Parameter, Direction,
    Property)


class Memento(object):
    @cached_method
    def caretaker(self):
        return Class('Caretaker', properties=[self.caretaker_memento()])

    @cached_method
    def memento(self):
        return Class('Memento')

    @cached_method
    def originator(self):
        return Class('Originator', operations=[
            self.originator_set_memento(),
            self.originator_create_memento(),
        ])

    @cached_method
    def caretaker_memento(self):
        return Property('memento', self.memento_type(), Visibility.PUBLIC,
                        is_static=False)

    @cached_method
    def originator_set_memento(self):
        return Operation(
            'set_memento', visibility=Visibility.PUBLIC, parameters=[
                Parameter('memento', self.memento_type(), Direction.IN)
            ], is_static=False)

    @cached_method
    def originator_create_memento(self):
        return Operation('create_memento', self.memento_type(),
                         visibility=Visibility.PUBLIC, is_static=False)

    @cached_method
    def memento_type(self):
        return Type(self.memento())

    @cached_method
    def create(self):
        self.originator().suppliers = [self.memento()]
        return Model([
            self.caretaker(),
            self.memento(),
            self.originator(),
        ])


if __name__ == '__main__':
    print Memento().create()
