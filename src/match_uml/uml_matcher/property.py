# coding: utf-8

from graph_matcher import cached_eq
from uml_matcher.named_element import NamedElement
from uml_matcher.eq_pattern import eq_pattern, equiv_pattern, sub_equiv_pattern
from uml_matcher.has_equivalents import has_equivalents


class Property(NamedElement):
    def __init__(self, type,
                 name='anonymous',
                 visibility=None,
                 aggregation=None,
                 is_derived=None,
                 is_derived_union=None,
                 is_id=None,
                 is_leaf=None,
                 is_read_only=None,
                 is_static=None,
                 subsetted_properties=tuple(),
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
        self.subsetted_properties = subsetted_properties
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
                                    pattern.subsetted_properties)
                and sub_equiv_pattern(self.type, pattern.type))

    @cached_eq
    def equiv_pattern(self, pattern):
        return (self.sub_equiv_pattern(pattern)
                and equiv_pattern(self.owner, pattern.owner))

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

    def __repr__(self):
        return ('{visibility}{owner}{name}'.format(
            visibility=self.visibility if self.visibility else '',
            name=self.name,
            owner='' if self.owner is None else '%s::' % self.owner,
        ))

    def __hash__(self):
        return id(self)
