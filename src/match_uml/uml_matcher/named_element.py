# coding: utf-8

from uml_matcher.element import Element


class NamedElement(Element):
    def __init__(self, name):
        super(NamedElement, self).__init__()
        self.name = name

    def __str__(self):
        return 'named element %s' % self.name

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.name))

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, NamedElement)
                and self.name == other.name)
