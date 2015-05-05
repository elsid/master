# coding: utf-8

from uml_matcher.cached_method import cached_method


class Element(object):
    @cached_method
    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return hash(self) < hash(other)
