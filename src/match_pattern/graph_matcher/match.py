# coding: utf-8

import logging

from collections import defaultdict
from heapq import heappush, heappop
from itertools import tee, combinations, permutations, izip, product
from graph_matcher.configuration import Configuration, Equivalent


class PriorityQueue(object):
    def __init__(self):
        self.__queue = []
        self.__index = 0

    def append(self, item, priority):
        heappush(self.__queue, (-priority, self.__index, item))
        self.__index += 1

    def pop(self):
        return heappop(self.__queue)[-1]

    def __len__(self):
        return len(self.__queue)

    def __nonzero__(self):
        return bool(self.__queue)

    def __getitem__(self, item):
        return self.__queue[item][-1]


def replace_node_by_obj(value):
    if hasattr(value, 'target') and hasattr(value, 'pattern'):
        return type(value)(value.target.obj, value.pattern.obj)
    else:
        return (replace_node_by_obj(x) for x in value)


def generate_equivalent_one_node_pairs(target_nodes, pattern_node):
    for target in sorted(target_nodes):
        if target.equiv_pattern(pattern_node):
            yield target, pattern_node


def generate_equivalent_node_pairs(target_nodes, pattern_nodes):
    for target, pattern in product(sorted(target_nodes), sorted(pattern_nodes)):
        if target.equiv_pattern(pattern):
            yield target, pattern


def generate_chains(target_nodes, pattern_nodes):

    def generate_pairs():
        return generate_equivalent_node_pairs(target_nodes, pattern_nodes)

    def make_pattern_dict():
        result = defaultdict(set)
        for target, pattern in generate_pairs():
            result[pattern].add(target)
        return result

    pattern_dict = make_pattern_dict()

    def generate(pattern_iter, chain):
        try:
            pattern, targets = next(pattern_iter)
            not_used_targets = sorted(targets - {x.target for x in chain})
            pattern_iter_list = tee(pattern_iter, len(not_used_targets))
            for new_iter, target in izip(pattern_iter_list, not_used_targets):
                new_chain = chain + [Equivalent(target, pattern)]
                for sub_chain in generate(new_iter, new_chain):
                    yield sub_chain
        except StopIteration:
            yield chain

    return generate(iter(sorted(pattern_dict.iteritems())), list())


class ConfigurationsGenerator(object):
    def __init__(self, initial_variants, pattern_nodes_count):
        self.__pattern_nodes_count = pattern_nodes_count
        self.__generators = PriorityQueue()
        self.__result = []
        self.__generators.append(initial_variants, 1)
        logging.debug('add generator %d with priority %d and checked len %d',
                      len(self.__generators), 1, 1)

    def __iter__(self):
        return self

    def next(self):
        while self.__generators:
            try:
                return next(self.__generators[0])
            except StopIteration:
                self.__generators.pop()
                logging.debug('pop generator %d', len(self.__generators))
        raise StopIteration

    def generate(self, configuration):

        def priority():
            return (self.__pattern_nodes_count * len(configuration.checked)
                    + configuration.count_remaining_selected())

        def generate():
            new_configurations_generated = False
            for chain in generate_chains(configuration.target.neighbors,
                                         configuration.pattern.neighbors):
                chain = configuration.filter(chain)
                if chain:
                    new_conf = configuration.clone(chain)
                    yield new_conf
                    new_configurations_generated = True
            if not new_configurations_generated:
                yield configuration

        self.__generators.append(generate(), priority())
        logging.debug('add generator %d with priority %d and checked len %d',
                      len(self.__generators), priority(),
                      len(configuration.checked))

    def add_result(self, configuration):
        if configuration.checked not in self.__result:
            self.__result.append(configuration.checked)
            logging.debug('add result %d', len(self.__result))
            return True


def match_one(target_graph, pattern_graph):
    logging.info('match single components graphs')
    log_graph_stats(pattern_graph, 'pattern')
    log_graph_stats(target_graph, 'target')

    if not pattern_graph.nodes:
        return

    def generate_initial():
        return generate_equivalent_one_node_pairs(
            target_graph.nodes, pattern_graph.least_connected_node)

    def generate_initial_configurations():
        for t, p in generate_initial():
            for chain in generate_chains(t.neighbors, p.neighbors):
                yield Configuration(t, p, chain)

    configurations = ConfigurationsGenerator(generate_initial_configurations(),
                                             len(pattern_graph.nodes))
    for configuration in configurations:
        logging.debug('process configuration %s', configuration)
        configuration.advance()
        if configuration.at_end():
            checked_patterns = configuration.checked_patterns
            if len(checked_patterns) == len(pattern_graph.nodes):
                if configurations.add_result(configuration):
                    logging.debug('result configuration %s', configuration)
                    yield sorted(configuration.checked)
                else:
                    logging.debug('duplicate result configuration %s',
                                  configuration)
            else:
                not_found = (frozenset(x for x in pattern_graph.nodes)
                             - checked_patterns)
                logging.debug('drop configuration %s; not found %s',
                              configuration,
                              ', '.join(str(x.obj) for x in sorted(not_found)))
        else:
            configurations.generate(configuration)


def match_one_pattern(pattern_graph, target_components):
    graph_type = type(pattern_graph)
    for component in target_components:
        for v in match_one(graph_type(nodes=component), pattern_graph):
            yield v


def match_one_target(target_graph, pattern_components):
    graph_type = type(target_graph)
    for component in pattern_components:
        for v in match_one(target_graph, graph_type(nodes=component)):
            yield v


def match_many(more_components, less_components, match_one_in_many, graph_type):
    less_n = len(less_components)

    def match_combination(more_components_combination):
        local_result = []
        for more_component in more_components_combination:
            more_graph = graph_type(nodes=more_component)
            for p in permutations(less_components, less_n):
                for v in match_one_in_many(more_graph, p):
                    if v not in local_result:
                        local_result.append(v)
                        yield v

    more_combinations = combinations(more_components, less_n)
    result = []

    def generate_merged_variants(variants):
        variants = tuple(variants)
        for n in xrange(len(variants), 0, -1):
            local_result = []
            for variants_combination in combinations(variants, n):
                union = unite_variants(variants_combination)
                if union:
                    union = sorted(union)
                    if union not in result and union not in local_result:
                        local_result.append(union)
                        yield union
            if local_result:
                result.extend(local_result)
                return

    for combination in (match_combination(x) for x in more_combinations):
        merged_variants = generate_merged_variants(combination)
        for variant in merged_variants:
            yield variant


def match(target_graph, pattern_graph):
    assert type(target_graph) == type(pattern_graph)
    logging.info('match graphs')
    log_graph_stats(pattern_graph, 'pattern')
    log_graph_stats(target_graph, 'target')
    graph_type = type(target_graph)
    pattern_components = tuple(pattern_graph.connected_components)
    target_components = tuple(target_graph.connected_components)
    target_n = len(target_components)
    pattern_n = len(pattern_components)
    if target_n <= 1:
        if pattern_n <= 1:
            return match_one(target_graph, pattern_graph)
        else:
            return match_one_target(target_graph, pattern_components)
    else:
        if pattern_n <= 1:
            return match_one_pattern(pattern_graph, target_components)
        elif pattern_n <= target_n:
            return match_many(target_components, pattern_components,
                              match_one_target, graph_type)
        else:
            return match_many(pattern_components, target_components,
                              match_one_pattern, graph_type)


def unite_variants(variants):
    if not variants:
        return None
    elif len(variants) == 1:
        return variants[0]
    elif len(variants) == 2:
        return unite_two_variants_sets(variants[0], variants[1])
    else:
        union = variants[0]
        for variants_set in variants[1:]:
            union = unite_two_variants_sets(union, variants_set)
            if not union:
                return None
        return union


def unite_two_variants_sets(first, second):
    if {x.target for x in first} & {x.target for x in second}:
        return None
    if {x.pattern for x in first} & {x.pattern for x in second}:
        return None
    return first + second


def log_graph_stats(graph, name):
    logging.info(
        '%s graph has %d nodes, %d arcs, %s connected components (nodes)%s',
        name, len(graph.nodes), count_arcs(graph),
        '%s (%s)' % count_connected_components(graph),
        ', least connected node is %s' % graph.least_connected_node
        if graph.nodes else '')


def count_arcs(graph):
    return sum(sum(len(x.incoming) + len(x.outgoing)
                   for x in n.connections.values()) for n in graph.nodes)


def count_connected_components(graph):
    components = tuple(graph.connected_components)
    return len(components), ', '.join(str(len(x)) for x in components)
