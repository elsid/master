# coding: utf-8

import yaml
from itertools import izip
from utils import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.eq_pattern import eq_pattern


class Operation(NamedElement):
    def __init__(self,
                 name=None,
                 result=None,
                 visibility=None,
                 parameters=None,
                 is_static=None,
                 invocations=None,
                 owner=None):
        super(Operation, self).__init__(name)
        self.result = result
        self.visibility = visibility
        self.__parameters = list(parameters) if parameters else list()
        self.is_static = is_static
        self.invocations = list(invocations) if invocations else list()
        self.owner = owner
        self.__update_parameters()

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value
        self.__update_parameters()

    @property
    def full_name(self):
        return '%s::%s' % (self.owner.full_name, self.name)

    @cached_eq
    def equiv_pattern(self, pattern):
        return (super(Operation, self).equiv_pattern(pattern)
                and eq_pattern(self.visibility, pattern.visibility)
                and eq_pattern(self.is_static, pattern.is_static))

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Operation, self).__eq__(other)
                and isinstance(other, Operation)
                and self.visibility == other.visibility
                and self.result == other.result
                and self.parameters == other.parameters
                and self.is_static == other.is_static)

    def __str__(self):

        def str_param(value):
            return '{direction}{name}{type}'.format(
                name=value.name,
                type=': %s' % value.type.name if value.type else '',
                direction='%s ' % value.direction if value.direction else '',
            )

        return ('{visibility}{owner}{name}({parameters}){result}{is_static}'
                .format(
                    visibility=self.visibility if self.visibility else '',
                    name=self.name,
                    result=': %s' % self.result.name if self.result else '',
                    parameters=', '.join(str_param(x) for x in self.parameters),
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
            is_static=value.is_static,
            invocations=value.invocations or None,
            owner=value.owner,
        )

    def is_overridden(self, operation):

        def is_substitutable(parameters):
            if len(self.parameters) != len(parameters):
                return False
            for p1, p2 in izip(self.parameters, parameters):
                if p1.type != p2.type and p1.direction != p2.direction:
                    return False
            return True

        return (isinstance(operation, Operation)
                and self.name == operation.name
                and self.result == operation.result
                and is_substitutable(operation.parameters))

    def __update_parameters(self):
        for parameter in self.__parameters:
            parameter.owner = self


yaml.add_representer(Operation, Operation.yaml_representer)
yaml.add_constructor('!Operation', Operation.yaml_constructor)
