# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.eq_pattern import eq_pattern


class Parameter(NamedElement):
    def __init__(self, name=None, type=None, direction=None, position=None,
                 owner=None):
        super(Parameter, self).__init__(name)
        assert position is None or position > 0
        self.type = type
        self.direction = direction
        self.__position = position
        self.owner = owner

    @cached_eq
    def equiv_pattern(self, pattern):
        return (super(Parameter, self).equiv_pattern(pattern)
                and eq_pattern(self.direction, pattern.direction)
                and eq_pattern(self.position, pattern.position))

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Parameter, self).__eq__(other)
                and isinstance(other, Parameter)
                and self.type == other.type
                and self.direction == other.direction
                and self.position == other.position)

    def __str__(self):
        return '{position}{direction}{name}{type}{owner}'.format(
            position='%dth ' % self.position if self.position else '',
            name=self.name,
            type=': %s' % self.type.name if self.type else '',
            direction='%s ' % self.direction if self.direction else '',
            owner=' of %s' % self.owner if self.owner else '',
        )

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        assert value is None or value > 0
        self.__position = value

    @staticmethod
    def yaml_representer(dumper, value):
        return Parameter._yaml_representer(
            dumper, value,
            type=value.type,
            direction=value.direction,
            position=value.position,
            owner=value.owner,
        )


yaml.add_representer(Parameter, Parameter.yaml_representer)
yaml.add_constructor('!Parameter', Parameter.yaml_constructor)
