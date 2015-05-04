# coding: utf-8

from collections import namedtuple
from itertools import islice
from graph_matcher import Graph, Equivalent
from graph_matcher.match import EndType
from uml_matcher.errors import CheckVariantFailed


class MatchVariant(object):
    def __init__(self, equivalents=None):
        self.equivalents = (tuple(equivalents) if equivalents else tuple())

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchVariant)
                and eq_ignore_order(self.equivalents, other.equivalents))

    def __repr__(self):
        return '\n'.join('%s === %s' % (x.target, x.pattern)
                         for x in self.equivalents)

    def __len__(self):
        return len(self.equivalents)

    def __contains__(self, item):
        return isinstance(item, tuple) and item in self.equivalents


class MatchResult(object):
    def __init__(self, variants=None):
        self.variants = tuple(variants) if variants else tuple()

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchResult)
                and eq_ignore_order(self.variants, other.variants))

    def __repr__(self):
        return '\n'.join('%s\n' % repr(x) for x in self.variants)

    def __len__(self):
        return len(self.variants)

    def __contains__(self, item):
        return isinstance(item, MatchVariant) and item in self.variants


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


Generalization = namedtuple('Generalization', ('derived', 'general'))
Dependency = namedtuple('Dependency', ('client', 'supplier'))
HasProperty = namedtuple('HasProperty', ('classifier', 'property'))
HasOperation = namedtuple('HasOperation', ('classifier', 'operation'))
PropertyIs = namedtuple('PropertyIs', ('property', 'type'))


class BinaryAssociation(frozenset):
    def __init__(self, ends):
        assert len(ends) == 2
        super(BinaryAssociation, self).__init__(ends)


def make_graph(diagram):

    def generate():
        for classifier in diagram.classifiers:
            for general in classifier.generals:
                yield Generalization(derived=classifier, general=general)
            for supplier in classifier.suppliers:
                yield Dependency(client=classifier, supplier=supplier)
            for property_ in classifier.properties:
                yield HasProperty(classifier, property_)
                yield PropertyIs(property_, property_.type)
                for association in property_.associations:
                    yield BinaryAssociation({property_, association})
                    yield PropertyIs(association, association.type)
            for operation in classifier.operations:
                yield HasOperation(classifier, operation)

    return Graph(generate())


def match(target, pattern, limit=None):
    target_graph = make_graph(target)
    pattern_graph = make_graph(pattern)
    result = islice(target_graph.match(pattern_graph), limit)
    return MatchResult(MatchVariant(replace_nodes_by_objs(x))
                       for x in result if check(x))


Connection = namedtuple('Connection', ('color', 'end_type', 'node'))


def check(equivalents, raise_if_false=True):
    equivalents = tuple(equivalents)
    all_target_nodes = frozenset(x.target for x in equivalents)
    used = set()

    def has_pattern(connection_color, end_type, pattern_node):

        def has_equivalent(target_nodes):
            for target_node in target_nodes & all_target_nodes:
                if Equivalent(target_node, pattern_node) in equivalents:
                    return True

        for tk, tv in equivalent.target.connections.iteritems():
            if connection_color == tk:
                if end_type == EndType.incoming:
                    return has_equivalent(tv.incoming)
                elif end_type == EndType.outgoing:
                    return has_equivalent(tv.outgoing)

    def check_pattern_nodes(connection_color, end_type, nodes):
        for node in nodes:
            connection = Connection(connection_color, end_type, node)
            if connection not in used:
                if has_pattern(*connection):
                    used.add(connection)
                else:
                    if raise_if_false:
                        e = Equivalent(equivalent.target.obj,
                                       equivalent.pattern.obj)
                        raise CheckVariantFailed(
                            MatchVariant(replace_nodes_by_objs(equivalents)),
                            e, connection)
                    else:
                        return False
        return True

    for equivalent in equivalents:
        for pk, pv in equivalent.pattern.connections.iteritems():
            if not check_pattern_nodes(pk, EndType.incoming, pv.incoming):
                return False
            if not check_pattern_nodes(pk, EndType.outgoing, pv.outgoing):
                return False
    return True


def replace_nodes_by_objs(equivalents):
    return (Equivalent(x.target.obj, x.pattern.obj) for x in equivalents)
