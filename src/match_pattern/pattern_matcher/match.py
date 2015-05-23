# coding: utf-8

from collections import namedtuple, deque
from itertools import islice
from graph_matcher import Graph, Equivalent
from graph_matcher.configuration import EndType
from pattern_matcher.errors import CheckVariantFailed


class MatchVariant(object):
    def __init__(self, equivalents=None):
        self.equivalents = tuple(equivalents) if equivalents else tuple()

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchVariant)
                and eq_ignore_order(self.equivalents, other.equivalents))

    def __str__(self):
        return '\n'.join(str(x) for x in self.equivalents)

    def __repr__(self):
        e = ',\n'.join(repr(x) for x in self.equivalents)
        return 'MatchVariant(%s)' % ('[\n%s\n]' % e if e else '')

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

    def __str__(self):
        return '\n\n'.join(str(x) for x in self.variants)

    def __repr__(self):
        v = ',\n'.join(repr(x) for x in self.variants)
        return 'MatchResult(%s)' % ('[\n%s\n]' % v if v else '')

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

    def find_eq(first_value):

        def can_be_used(index, value):
            return (index not in used
                    and (eq_ignore_order(first_value, value)
                         if is_list(value) else first_value == value))

        for second_index, second_value in enumerate(second):
            if can_be_used(second_index, second_value):
                used.add(second_index)
                return True

    for x in first:
        if not find_eq(x):
            return False
    return True


Generalization = namedtuple('Generalization', ('derived', 'general'))
Dependency = namedtuple('Dependency', ('client', 'supplier'))
HasProperty = namedtuple('HasProperty', ('classifier', 'property'))
HasOperation = namedtuple('HasOperation', ('classifier', 'operation'))
PropertyType = namedtuple('PropertyType', ('property', 'type'))
OperationResult = namedtuple('OperationResult', ('operation', 'type'))
TypeClassifier = namedtuple('TypeClassifier', ('classifier', 'type'))
Invocation = namedtuple('Invocation', ('invoker', 'invoked'))
Overriding = namedtuple('Overriding', ('override', 'overridden'))
HasParameter = namedtuple('HasParameter', ('operation', 'parameter'))
ParameterType = namedtuple('ParameterType', ('parameter', 'type'))


def make_graph(model):

    def generate():
        for classifier in model.classifiers:
            for general in classifier.generals:
                yield Generalization(derived=classifier, general=general)
            for supplier in classifier.suppliers:
                yield Dependency(client=classifier, supplier=supplier)
            for property_ in classifier.properties:
                yield HasProperty(classifier, property_)
                yield PropertyType(property_, property_.type)
                yield TypeClassifier(property_.type, property_.type.classifier)
            for operation in classifier.operations:
                yield HasOperation(classifier, operation)
                if operation.result:
                    yield OperationResult(operation, operation.result)
                    yield TypeClassifier(operation.result,
                                         operation.result.classifier)
                for invocation in operation.invocations:
                    yield Invocation(operation, invocation)
                overridden = find_overridden(operation)
                if overridden:
                    yield Overriding(operation, overridden)
                for parameter in operation.parameters:
                    yield HasParameter(operation, parameter)
                    yield ParameterType(parameter, parameter.type)
                    yield TypeClassifier(parameter.type,
                                         parameter.type.classifier)

    return Graph(generate())


def find_overridden(operation):
    visited = set()
    generals = deque(operation.owner.generals)
    while generals:
        classifier = generals.popleft()
        visited.add(classifier)
        overridden = classifier.get_overridden_operation(operation)
        if overridden:
            return overridden
        for general in classifier.generals:
            if general not in visited:
                visited.add(general)
                generals.append(general)


def match(target, pattern, limit=None, all_components=False):
    target_graph = make_graph(target)
    pattern_graph = make_graph(pattern)
    result = islice(target_graph.match(pattern_graph, not all_components),
                    limit)
    return MatchResult(MatchVariant(replace_nodes_by_objs(x))
                       for x in result if check(x))


Connection = namedtuple('Connection', ('color', 'end_type', 'node'))


def check(equivalents, raise_if_false=True):
    equivalents = tuple(equivalents)
    all_target_nodes = frozenset(x.target for x in equivalents)
    used = set()

    def check_one(equivalent):

        def has_pattern(connection):

            def has_equivalent(target_nodes):
                for target_node in target_nodes & all_target_nodes:
                    if Equivalent(target_node, connection.node) in equivalents:
                        return True

            for tk, tv in equivalent.target.connections.iteritems():
                if connection.color == tk:
                    if connection.end_type == EndType.INCOMING:
                        return has_equivalent(tv.incoming)
                    elif connection.end_type == EndType.OUTGOING:
                        return has_equivalent(tv.outgoing)

        def check_pattern_nodes(connection_color, end_type, nodes):
            for node in nodes:
                connection = Connection(connection_color, end_type, node)
                if connection not in used:
                    if has_pattern(connection):
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

        for pk, pv in equivalent.pattern.connections.iteritems():
            if not check_pattern_nodes(pk, EndType.INCOMING, pv.incoming):
                return False
            if not check_pattern_nodes(pk, EndType.OUTGOING, pv.outgoing):
                return False
        return True

    for x in equivalents:
        if not check_one(x):
            return False
    return True


def replace_nodes_by_objs(equivalents):
    return (Equivalent(x.target.obj, x.pattern.obj) for x in equivalents)
