# coding: utf-8

from collections import namedtuple, deque
from itertools import islice, tee
from graph_matcher import Graph, check, replace_node_by_obj


class MatchVariant(object):
    def __init__(self, isomorphism=None):
        self.isomorphism = tuple(isomorphism) if isomorphism else tuple()

    def as_dot(self):
        from pattern_matcher.model import Model
        from pattern_matcher.classifier import Classifier
        pattern_model = Model(x.pattern for x in self.isomorphism
                              if isinstance(x.pattern, Classifier))
        pattern_graph = pattern_model.graph().as_dot('MatchVariant')
        for x in self.isomorphism:
            node = pattern_graph.get_node('"%s"' % str(x.pattern))[0]
            node.set('label', '<<%s>>\n%s\n%s' % (
                type(x.pattern).__name__, x.pattern.full_name,
                x.target.full_name))
        return pattern_graph

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

    def __iter__(self):
        return iter(self.isomorphism)


class MatchResult(object):
    def __init__(self, variants=None):
        self.__variants = (iter(variants)
                           if variants is not None else iter(tuple()))

    @property
    def variants_iter(self):
        self.__variants, variants = tee(self.__variants)
        return variants

    @property
    def variants(self):
        return tuple(self.variants_iter)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchResult)
                and eq_ignore_order(self.variants, other.variants))

    def __str__(self):
        return '\n\n'.join(str(x) for x in self.variants_iter)

    def __repr__(self):
        v = ',\n'.join(repr(x) for x in self.variants_iter)
        return 'MatchResult(%s)' % ('[\n%s\n]' % v if v else '')

    def __len__(self):
        return len(self.variants)

    def __contains__(self, item):
        return isinstance(item, MatchVariant) and item in self.variants_iter

    def __iter__(self):
        return self.variants_iter


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
                for general in all_indirect_generals(classifier):
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
                    if Dependency in use_connections:
                        yield Dependency(classifier,
                                         operation.result.classifier)
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
                    if Dependency in use_connections:
                        yield Dependency(classifier, parameter.type.classifier)
                    if HasParameter in use_connections:
                        yield HasParameter(operation, parameter)
                    if ParameterType in use_connections:
                        yield ParameterType(parameter, parameter.type)
                    if TypeClassifier in use_connections:
                        yield TypeClassifier(parameter.type,
                                             parameter.type.classifier)

    return Graph(generate())


def find_overridden(operation):
    for classifier in all_indirect_generals(operation.owner):
        overridden = classifier.get_overridden_operation(operation)
        if overridden:
            return overridden


def all_indirect_generals(classifier):
    visited = set(classifier.generals)
    generals = deque(classifier.generals)
    while generals:
        classifier = generals.popleft()
        yield classifier
        for general in classifier.generals:
            if general not in visited:
                visited.add(general)
                generals.append(general)


def match(target, pattern, limit=None):
    pattern_graph = make_graph(pattern)
    target_graph = make_graph(target, pattern_graph.connections_types)
    result = islice(target_graph.match(pattern_graph), limit)
    return MatchResult(MatchVariant(replace_node_by_obj(x))
                       for x in result if check(x))
