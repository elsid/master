# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.eq_pattern import eq_pattern, sub_equiv_pattern
from pattern_matcher.has_equivalents import has_equivalents


class Property(NamedElement):
    def __init__(self,
                 type=None,
                 name=None,
                 visibility=None,
                 aggregation=None,
                 is_derived=None,
                 is_derived_union=None,
                 is_id=None,
                 is_leaf=None,
                 is_read_only=None,
                 is_static=None,
                 subsetted_properties=None,
                 owner=None):
        super(Property, self).__init__(name)
        self.type = type
        self.visibility = visibility
        self.aggregation = aggregation
        self.is_derived = is_derived
        self.is_derived_union = is_derived_union
        self.is_id = is_id
        self.is_leaf = is_leaf
        self.is_read_only = is_read_only
        self.is_static = is_static
        self.subsetted_properties = (list(subsetted_properties)
                                     if subsetted_properties else list())
        self.owner = owner

    @cached_eq
    def sub_equiv_pattern(self, pattern):
        return (isinstance(pattern, Property)
                and eq_pattern(self.visibility, pattern.visibility)
                and eq_pattern(self.aggregation, pattern.aggregation)
                and eq_pattern(self.is_derived, pattern.is_derived)
                and eq_pattern(self.is_derived_union, pattern.is_derived_union)
                and eq_pattern(self.is_id, pattern.is_id)
                and eq_pattern(self.is_leaf, pattern.is_leaf)
                and eq_pattern(self.is_read_only, pattern.is_read_only)
                and eq_pattern(self.is_static, pattern.is_static)
                and has_equivalents(self.subsetted_properties,
                                    pattern.subsetted_properties))

    @cached_eq
    def equiv_pattern(self, pattern):
        return self.sub_equiv_pattern(pattern)

    def sub_eq(self, other):
        return (id(self) == id(other)
                or isinstance(other, Property)
                and self.visibility == other.visibility
                and self.aggregation == other.aggregation
                and self.is_derived == other.is_derived
                and self.is_derived_union == other.is_derived_union
                and self.is_id == other.is_id
                and self.is_leaf == other.is_leaf
                and self.is_read_only == other.is_read_only
                and self.is_static == other.is_static
                and self.subsetted_properties == other.subsetted_properties)

    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Property, self).__eq__(other)
                and isinstance(other, Property)
                and self.sub_eq(other)
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
            is_derived=value.is_derived,
            is_derived_union=value.is_derived_union,
            is_id=value.is_id,
            is_leaf=value.is_leaf,
            is_read_only=value.is_read_only,
            is_static=value.is_static,
            subsetted_properties=value.subsetted_properties or None,
        )


yaml.add_representer(Property, Property.yaml_representer)
yaml.add_constructor('!Property', Property.yaml_constructor)