#!/usr/bin/env python3
# coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.visibility import Visibility
from uml_matcher.has_equivalents import has_equivalents


class Operation(NamedElement):
    def __init__(self,
                 name='anonymous',
                 visibility=Visibility.public,
                 result=None,
                 parameters=tuple(),
                 is_leaf=False,
                 is_query=False,
                 is_static=False):
        self.name = name
        self.visibility = visibility
        self.result = result
        self.parameters = parameters
        self.is_leaf = is_leaf
        self.is_query = is_query
        self.is_static = is_static

    def sub_equivalent_pattern(self, pattern):
        return (self.visibility == pattern.visibility
                and (self.result is None
                     or self.result.sub_equivalent_pattern(pattern.result))
                and has_equivalents(self.parameters, pattern.parameters)
                and self.is_leaf == pattern.is_leaf
                and self.is_query == pattern.is_query
                and self.is_static == pattern.is_static)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, type(self))
                and self.name == self.name
                and self.visibility == other.visibility
                and self.result == other.result
                and self.parameters == other.parameters
                and self.is_leaf == other.is_leaf
                and self.is_query == other.is_query
                and self.is_static == other.is_static)

    def __repr__(self):
        return ('{visibility}{name}({parameters}){result} {is_leaf} {is_query} '
                '{is_static}'
                .format(
                    visibility=self.visibility,
                    name=self.name,
                    result=': ' + repr(self.result) if self.result else '',
                    parameters=', '.join(map(str, self.parameters)),
                    is_leaf='leaf' if self.is_leaf else '',
                    is_query='query' if self.is_query else '',
                    is_static='static' if self.is_static else ''))
