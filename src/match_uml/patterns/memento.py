# coding: utf-8

from uml_matcher import (
    Class, Type, Operation, Diagram, Visibility, Parameter, Direction,
    Property, cached_method)


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
        return Property(self.memento_type(), 'memento', Visibility.public,
                        is_static=False)

    @cached_method
    def originator_set_memento(self):
        return Operation(None, 'set_memento', Visibility.public, [
            Parameter(self.memento_type(), 'memento', Direction.in_)
        ], is_static=False)

    @cached_method
    def originator_create_memento(self):
        return Operation(None, 'create_memento', Visibility.public,
                         is_static=False)

    @cached_method
    def memento_type(self):
        return Type(self.memento())

    @cached_method
    def diagram(self):
        self.originator().suppliers = [self.memento()]
        return Diagram([
            self.caretaker(),
            self.memento(),
            self.originator(),
        ])


if __name__ == '__main__':
    print Memento().diagram()