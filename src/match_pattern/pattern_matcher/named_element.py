# coding: utf-8

from pattern_matcher.element import Element


class NamedElement(Element):
    __next_number = 0

    def __init__(self, name):
        super(NamedElement, self).__init__()
        if name:
            self.name = name
        else:
            self.name = 'anonymous_%d' % NamedElement.__next_number
            NamedElement.__next_number += 1

    def __str__(self):
        return 'named element %s' % self.name

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.name))

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, NamedElement)
                and self.name == other.name)

    @staticmethod
    def _yaml_representer(dumper, value, **kwargs):
        return Element._yaml_representer(dumper, value, name=str(value.name),
                                         **kwargs)

    @property
    def full_name(self):
        return self.name
