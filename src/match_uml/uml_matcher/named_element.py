#coding: utf-8

class NamedElement(object):
    def __lt__(self, other):
        return id(self) < id(other)
