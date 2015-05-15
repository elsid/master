#!/usr/bin/env python
# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.has_equivalents import has_equivalents
from pattern_matcher.eq_pattern import eq_pattern


class Operation(NamedElement):
    def __init__(self,
                 result=None,
                 name=None,
                 visibility=None,
                 parameters=None,
                 is_leaf=None,
                 is_query=None,
                 is_static=None,
                 invocations=None,
                 overridden=None,
                 owner=None):
        super(Operation, self).__init__(name)
        self.visibility = visibility
        self.result = result
        self.parameters = list(parameters) if parameters else list()
        self.is_leaf = is_leaf
        self.is_query = is_query
        self.is_static = is_static
        self.invocations = list(invocations) if invocations else list()
        self.overridden = overridden
        self.owner = owner

    @cached_eq
    def sub_equiv_pattern(self, pattern):
        return (isinstance(pattern, Operation)
                and eq_pattern(self.visibility, pattern.visibility)
                and has_equivalents(self.parameters, pattern.parameters)
                and eq_pattern(self.is_leaf, pattern.is_leaf)
                and eq_pattern(self.is_query, pattern.is_query)
                and eq_pattern(self.is_static, pattern.is_static))

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Operation, self).__eq__(other)
                and isinstance(other, Operation)
                and self.visibility == other.visibility
                and self.result == other.result
                and self.parameters == other.parameters
                and self.is_leaf == other.is_leaf
                and self.is_query == other.is_query
                and self.is_static == other.is_static)

    def __str__(self):
        return ('{visibility}{owner}{name}({parameters}){result}'
                '{is_leaf}{is_query}{is_static}'
                .format(
                    visibility=self.visibility if self.visibility else '',
                    name=self.name,
                    result=': %s' % self.result.name if self.result else '',
                    parameters=', '.join(map(str, self.parameters)),
                    is_leaf=' leaf' if self.is_leaf else '',
                    is_query=' query' if self.is_query else '',
                    is_static=' static' if self.is_static else '',
                    owner='%s::' % self.owner.name if self.owner else '',
                ))

    @staticmethod
    def yaml_representer(dumper, value):
        return Operation._yaml_representer(
            dumper, value,
            result=value.result,
            visibility=value.visibility,
            parameters=value.parameters or None,
            is_leaf=value.is_leaf,
            is_query=value.is_query,
            is_static=value.is_static,
            invocations=value.invocations or None,
            overridden=value.overridden,
        )


yaml.add_representer(Operation, Operation.yaml_representer)
yaml.add_constructor('!Operation', Operation.yaml_constructor)
