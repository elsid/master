# coding: utf-8


class NamedElement(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, NamedElement)
                and self.name == other.name)

    def __lt__(self, other):
        return self.name < other.name
