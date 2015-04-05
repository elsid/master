# coding: utf-8

from collections import namedtuple
from graph_matcher import Graph, replace_node_by_obj


BaseMatchVariant = namedtuple('BaseMatchVariant',
                              ('generalizations', 'associations'))


class MatchVariant(BaseMatchVariant):
    def __new__(cls, generalizations=tuple(), associations=tuple()):
        return super(MatchVariant, cls).__new__(cls, tuple(generalizations),
                                                tuple(associations))

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
    generalizations_variants = replace_node_by_obj(
        Graph(target.generalizations).match(Graph(pattern.generalizations)))
    associations_variants = replace_node_by_obj(
        Graph(target.associations).match(Graph(pattern.associations)))
    return MatchResult(combine(generalizations_variants, associations_variants))


def combine(generalizations_variants, associations_variants):
    if associations_variants:
        if generalizations_variants:

            def add(result, x):
                result += combine_association(generalizations_variants, x)
                return result

            return reduce(add, associations_variants, list())
        else:
            return (MatchVariant(associations=x) for x in associations_variants)
    elif generalizations_variants:
        return (MatchVariant(generalizations=x)
                for x in generalizations_variants)
    else:
        return tuple()


def combine_association(generalizations_variants, associations_variant):
    return (MatchVariant(generalizations=x, associations=associations_variant)
            for x in generalizations_variants
            if has_correspondence(x, associations_variant))


def has_correspondence(generalizations_variant, associations_variant):
    gt_classifiers = (x.target for x in generalizations_variant)
    at_classifiers = (x.target.type.classifier for x in associations_variant)
    gp_classifiers = (x.pattern for x in generalizations_variant)
    ap_classifiers = (x.pattern.type.classifier for x in associations_variant)
    return (frozenset(gt_classifiers) >= frozenset(at_classifiers)
            and frozenset(gp_classifiers) >= frozenset(ap_classifiers))
