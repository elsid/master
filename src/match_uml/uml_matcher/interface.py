# coding: utf-8


from uml_matcher.classifier import Classifier
from uml_matcher.cached_eq import cached_eq


class Interface(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Interface, self).__eq__(other)
                and isinstance(other, Interface))
