# coding: utf-8

from copy import copy
from graph_matcher import Graph, replace_node_by_obj


class Generalizations(tuple):
    def has_correspondence_with_associations(self, associations):
        return has_correspondence_with_associations(self, associations)

    def has_correspondence_with_dependencies(self, dependencies):
        return has_correspondence(self, dependencies)


class Dependencies(tuple):
    def has_correspondence_with_associations(self, associations):
        return has_correspondence_with_associations(self, associations)

    def has_correspondence_with_generalizations(self, generalizations):
        return has_correspondence(self, generalizations)


class Associations(tuple):
    pass


class MatchVariant(object):
    def __init__(self,
                 generalizations=tuple(),
                 dependencies=tuple(),
                 associations=tuple(),
                 current_attr=None):
        self.generalizations = Generalizations(generalizations)
        self.dependencies = Dependencies(dependencies)
        self.associations = Associations(associations)
        if current_attr:
            self.current_attr = current_attr
        elif self.generalizations:
            self.current_attr = 'generalizations'
        elif self.dependencies:
            self.current_attr = 'dependencies'
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
            elif isinstance(minor_variant.current, Dependencies):
                return self.current.has_correspondence_with_dependencies
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
                and eq_ignore_order(self.associations, other.associations)
                and eq_ignore_order(self.dependencies, other.dependencies))

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
            yield 'dependencies'
            if not self.dependencies:
                yield '  nothing'
            for x in self.dependencies:
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
        match_dependencies,
        match_associations,
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
        + list(associations_classifiers(target.associations))
        + list(dependencies_classifiers(target.dependencies)))
    pattern_graph = Graph(
        list(pattern.generalizations)
        + list(associations_classifiers(pattern.associations))
        + list(dependencies_classifiers(pattern.dependencies)))
    return [MatchVariant(generalizations=x)
            for x in replace_node_by_obj(target_graph.match(pattern_graph))]


def associations_classifiers(associations):
    for association in associations:
        for end in association:
            yield end.type.classifier


def dependencies_classifiers(dependencies):
    for dependency in dependencies:
        yield dependency.client
        yield dependency.supplier


def match_associations(target, pattern):
    target_graph = Graph(target.associations)
    pattern_graph = Graph(pattern.associations)
    return [MatchVariant(associations=x)
            for x in replace_node_by_obj(target_graph.match(pattern_graph))]


def match_dependencies(target, pattern):
    target_graph = Graph(target.dependencies)
    pattern_graph = Graph(pattern.dependencies)
    return [MatchVariant(dependencies=x)
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


def has_correspondence_with_associations(generalizations_or_dependencies,
                                         associations):
    t_classifiers = (x.target for x in generalizations_or_dependencies)
    at_classifiers = (x.target.type.classifier for x in associations)
    p_classifiers = (x.pattern for x in generalizations_or_dependencies)
    ap_classifiers = (x.pattern.type.classifier for x in associations)
    return (frozenset(t_classifiers) >= frozenset(at_classifiers)
            and frozenset(p_classifiers) >= frozenset(ap_classifiers))


def has_correspondence(major, minor):
    maj_t_classifiers = (x.target for x in major)
    min_t_classifiers = (x.target for x in minor)
    maj_p_classifiers = (x.pattern for x in major)
    min_p_classifiers = (x.pattern for x in minor)
    return (frozenset(maj_t_classifiers) >= frozenset(min_t_classifiers)
            and frozenset(maj_p_classifiers) >= frozenset(min_p_classifiers))
