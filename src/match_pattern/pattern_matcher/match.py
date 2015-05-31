# coding: utf-8

from collections import namedtuple, deque
from itertools import islice
from graph_matcher import Graph, Isomorphic
from graph_matcher.configuration import EndType
from pattern_matcher.errors import CheckVariantFailed


class MatchVariant(object):
    def __init__(self, isomorphism=None):
        self.isomorphism = tuple(isomorphism) if isomorphism else tuple()

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchVariant)
                and eq_ignore_order(self.isomorphism, other.isomorphism))

    def __str__(self):
        return '\n'.join(str(x) for x in self.isomorphism)

    def __repr__(self):
        e = ',\n'.join(repr(x) for x in self.isomorphism)
        return 'MatchVariant(%s)' % ('[\n%s\n]' % e if e else '')

    def __len__(self):
        return len(self.isomorphism)

    def __contains__(self, item):
        return isinstance(item, tuple) and item in self.isomorphism


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

CONNECTIONS_TYPES = frozenset((
    Generalization,
    Dependency,
    HasProperty,
    HasOperation,
    PropertyType,
    OperationResult,
    TypeClassifier,
    Invocation,
    Overriding,
    HasParameter,
    ParameterType,
))


def make_graph(model, use_connections=CONNECTIONS_TYPES):

    def generate():
        for classifier in model.classifiers:
            if Generalization in use_connections:
                for general in classifier.generals:
                    yield Generalization(derived=classifier, general=general)
            if Dependency in use_connections:
                for supplier in classifier.suppliers:
                    yield Dependency(client=classifier, supplier=supplier)
            for property_ in classifier.properties:
                if HasProperty in use_connections:
                    yield HasProperty(classifier, property_)
                if PropertyType in use_connections:
                    yield PropertyType(property_, property_.type)
                if TypeClassifier in use_connections:
                    yield TypeClassifier(property_.type,
                                         property_.type.classifier)
            for operation in classifier.operations:
                if HasOperation in use_connections:
                    yield HasOperation(classifier, operation)
                if operation.result:
                    if OperationResult in use_connections:
                        yield OperationResult(operation, operation.result)
                    if TypeClassifier in use_connections:
                        yield TypeClassifier(operation.result,
                                             operation.result.classifier)
                if Invocation in use_connections:
                    for invocation in operation.invocations:
                        yield Invocation(operation, invocation)
                if Overriding in use_connections:
                    overridden = find_overridden(operation)
                    if overridden:
                        yield Overriding(operation, overridden)
                for parameter in operation.parameters:
                    if HasParameter in use_connections:
                        yield HasParameter(operation, parameter)
                    if ParameterType in use_connections:
                        yield ParameterType(parameter, parameter.type)
                    if TypeClassifier in use_connections:
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
    pattern_graph = make_graph(pattern)
    target_graph = make_graph(target, pattern_graph.connections_types())
    result = islice(target_graph.match(pattern_graph, not all_components),
                    limit)
    return MatchResult(MatchVariant(replace_nodes_by_objs(x))
                       for x in result if check(x))


Connection = namedtuple('Connection', ('label', 'end_type', 'node'))


def check(isomorphism, raise_if_false=True):
    isomorphism = tuple(isomorphism)
    all_target_nodes = frozenset(x.target for x in isomorphism)
    used = set()

    def check_one(isomorphic):

        def has_pattern(connection):

            def has_equivalent(target_nodes):
                for target_node in target_nodes & all_target_nodes:
                    if Isomorphic(target_node, connection.node) in isomorphism:
                        return True

            for tk, tv in isomorphic.target.connections.iteritems():
                if connection.label == tk:
                    if connection.end_type == EndType.INCOMING:
                        return has_equivalent(tv.incoming)
                    elif connection.end_type == EndType.OUTGOING:
                        return has_equivalent(tv.outgoing)

        def check_pattern_nodes(connection_label, end_type, nodes):
            for node in nodes:
                connection = Connection(connection_label, end_type, node)
                if connection not in used:
                    if has_pattern(connection):
                        used.add(connection)
                    else:
                        if raise_if_false:
                            e = Isomorphic(isomorphic.target.obj,
                                           isomorphic.pattern.obj)
                            raise CheckVariantFailed(MatchVariant(
                                replace_nodes_by_objs(isomorphism)),
                                e, connection)
                        else:
                            return False
            return True

        for pk, pv in isomorphic.pattern.connections.iteritems():
            if not check_pattern_nodes(pk, EndType.INCOMING, pv.incoming):
                return False
            if not check_pattern_nodes(pk, EndType.OUTGOING, pv.outgoing):
                return False
        return True

    for x in isomorphism:
        if not check_one(x):
            return False
    return True


def replace_nodes_by_objs(isomorphism):
    return (type(x)(x.target.obj, x.pattern.obj) for x in isomorphism)
