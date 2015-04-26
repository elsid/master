# coding: utf-8

from copy import copy
from graph_matcher import Graph, replace_node_by_obj


class Generalizations(tuple):
    def has_correspondence_with_associations(self, associations):
        gt_classifiers = (x.target for x in self)
        at_classifiers = (x.target.type.classifier for x in associations)
        gp_classifiers = (x.pattern for x in self)
        ap_classifiers = (x.pattern.type.classifier for x in associations)
        return (frozenset(gt_classifiers) >= frozenset(at_classifiers)
                and frozenset(gp_classifiers) >= frozenset(ap_classifiers))


class Associations(tuple):
    pass


class MatchVariant(object):
    def __init__(self,
                 generalizations=tuple(),
                 associations=tuple(),
                 current_attr=None):
        self.generalizations = Generalizations(generalizations)
        self.associations = Associations(associations)
        if current_attr:
            self.current_attr = current_attr
        elif self.generalizations:
            self.current_attr = 'generalizations'
        elif self.associations:
            self.current_attr = 'associations'
        else:
            self.current_attr = None

    def new(self, minor_variant):
        self_copy = copy(self)
        setattr(self_copy, minor_variant.current_attr, minor_variant.current)
        return self_copy

    def has_correspondence(self, minor_variant):
        def get_func():
            if isinstance(minor_variant.current, Generalizations):
                return self.current.has_correspondence_with_generalizations
            elif isinstance(minor_variant.current, Associations):
                return self.current.has_correspondence_with_associations

        return get_func()(minor_variant.current)

    @property
    def current(self):
        return self.current_attr

    @current.getter
    def current(self):
        assert hasattr(self, self.current_attr)
        return getattr(self, self.current_attr)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchVariant)
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations))

    def __repr__(self):
        def gen():
            yield 'generalizations'
            if not self.generalizations:
                yield '  nothing'
            for x in self.generalizations:
                yield '  %s === %s' % (x.target, x.pattern)
            yield 'associations'
            if not self.associations:
                yield '  nothing'
            for x in self.associations:
                yield '  %s === %s' % (x.target, x.pattern)
        return '\n'.join(gen())


class MatchResult(object):
    def __init__(self, variants=tuple()):
        self.variants = tuple(variants)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchResult)
                and eq_ignore_order(self.variants, other.variants))

    def __repr__(self):
        return '\n'.join('%s\n' % repr(x) for x in self.variants)


def eq_ignore_order(first, second):

    def is_list(value):
        return isinstance(value, list)

    used = set()
    if len(first) != len(second):
        return False
    for x in first:
        found_eq = False

        def can_be_used(i, y):
            return (i not in used and (is_list(y) and eq_ignore_order(x, y) or
                    not is_list(y) and x == y))

        for i, y in enumerate(second):
            if can_be_used(i, y):
                used.add(i)
                found_eq = True
                break
        if not found_eq:
            return False
    return True


def match(target, pattern):
    pipeline = (
        match_generalizations,
        match_associations
    )

    def process(combined_variants, func):
        variants = func(target, pattern)
        if combined_variants:
            return combine(combined_variants, variants)
        else:
            return variants

    return MatchResult(reduce(process, pipeline, None))


def match_generalizations(target, pattern):
    target_graph = Graph(
        list(target.generalizations)
        + list(associations_classifiers(target.associations)))
    pattern_graph = Graph(
        list(pattern.generalizations)
        + list(associations_classifiers(pattern.associations)))
    return [MatchVariant(generalizations=x)
            for x in replace_node_by_obj(target_graph.match(pattern_graph))]


def associations_classifiers(associations):
    for association in associations:
        for end in association:
            yield end.type.classifier


def match_associations(target, pattern):
    target_graph = Graph(target.associations)
    pattern_graph = Graph(pattern.associations)
    return [MatchVariant(associations=x)
            for x in replace_node_by_obj(target_graph.match(pattern_graph))]


def combine(major_variants, minor_variants):
    def add(result, minor_variant):
        result += combine_one(major_variants, minor_variant)
        return result

    if minor_variants:
        return reduce(add, minor_variants, list())
    else:
        return major_variants


def combine_one(major_variants, minor_variant):
    for major_variant in major_variants:
        if major_variant.has_correspondence(minor_variant):
            yield major_variant.new(minor_variant)
