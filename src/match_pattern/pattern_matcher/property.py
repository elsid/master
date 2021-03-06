# coding: utf-8

import yaml
from utils import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.eq_pattern import eq_pattern


class Property(NamedElement):
    def __init__(self,
                 name=None,
                 type=None,
                 visibility=None,
                 aggregation=None,
                 is_static=None,
                 owner=None):
        super(Property, self).__init__(name)
        self.type = type
        self.visibility = visibility
        self.aggregation = aggregation
        self.is_static = is_static
        self.owner = owner

    @property
    def full_name(self):
        return '%s::%s' % (self.owner.full_name, self.name)

    @cached_eq
    def equiv_pattern(self, pattern):
        return (super(Property, self).equiv_pattern(pattern)
                and eq_pattern(self.visibility, pattern.visibility)
                and eq_pattern(self.aggregation, pattern.aggregation)
                and eq_pattern(self.is_static, pattern.is_static))

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Property, self).__eq__(other)
                and isinstance(other, Property)
                and self.visibility == other.visibility
                and self.aggregation == other.aggregation
                and self.is_static == other.is_static
                and self.type == other.type)

    def __str__(self):
        return '{visibility}{owner}{name}{type}'.format(
            visibility=self.visibility if self.visibility else '',
            name=self.name,
            owner='%s::' % self.owner.name if self.owner else '',
            type=': %s' % self.type.name if self.type else '',
        )

    @staticmethod
    def yaml_representer(dumper, value):
        return Property._yaml_representer(
            dumper, value,
            type=value.type,
            visibility=value.visibility,
            aggregation=value.aggregation,
            is_static=value.is_static,
            owner=value.owner,
        )


yaml.add_representer(Property, Property.yaml_representer)
yaml.add_constructor('!Property', Property.yaml_constructor)
