# coding: utf-8

from collections import defaultdict
from itertools import tee, combinations, permutations
from graph_matcher.configuration import Configuration, Equivalent


def replace_node_by_obj(variants):
    return ((Equivalent(x.target.obj, x.pattern.obj) for x in variant)
            for variant in variants)


def generate_equivalent_node_pairs(target_nodes, pattern_nodes):
    for target in sorted(target_nodes):
        for pattern in sorted(pattern_nodes):
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
            pattern = next(pattern_iter)
            not_used_targets = list(pattern_dict[pattern]
                                    - {x.target for x in chain})
            pattern_iter_list = tee(pattern_iter, len(not_used_targets))
            for index, target in enumerate(not_used_targets):
                new_chain = chain + [Equivalent(target, pattern)]
                for sub_chain in generate(pattern_iter_list[index], new_chain):
                    yield sub_chain
        except StopIteration:
            yield chain

    return generate(iter(sorted(pattern_dict.keys())), list())


class ConfigurationsGenerator(object):
    def __init__(self, initial_variants):
        self.__generators = [initial_variants]
        self.__result = []

    def __iter__(self):
        return self

    def next(self):
        while self.__generators:
            try:
                return next(self.__generators[-1])
            except StopIteration:
                self.__generators.pop()
        raise StopIteration

    def generate(self, configuration):

        def generate():
            new_configurations_generated = False
            for chain in generate_chains(configuration.target().neighbors(),
                                         configuration.pattern().neighbors()):
                chain = configuration.filter(chain)
                if chain:
                    new_conf = configuration.clone(chain)
                    if frozenset(new_conf.selected) not in self.__result:
                        new_conf.advance()
                        yield new_conf
                        new_configurations_generated = True
            if not new_configurations_generated:
                yield configuration

        self.__generators.append(generate())

    def add_result(self, configuration):
        if configuration.checked not in self.__result:
            self.__result.append(configuration.checked)
            return True


def match_one(target_graph, pattern_graph):
    def generate_initial():
        return generate_equivalent_node_pairs(target_graph.nodes,
                                              pattern_graph.nodes)

    def generate_initial_configurations():
        for t, p in generate_initial():
            for chain in generate_chains(t.neighbors(), p.neighbors()):
                yield Configuration(t, p, chain)

    configurations = ConfigurationsGenerator(generate_initial_configurations())
    for configuration in configurations:
        configuration.advance()
        if configuration.at_end():
            if configuration.checked_patterns() == pattern_graph.nodes:
                if configurations.add_result(configuration):
                    yield sorted(configuration.checked)
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


def match(target_graph, pattern_graph, match_largest_target_component=False):
    assert type(target_graph) == type(pattern_graph)
    graph_type = type(target_graph)
    target_components = tuple(target_graph.get_connected_components())
    pattern_components = tuple(pattern_graph.get_connected_components())
    if match_largest_target_component and len(target_components) > 0:
        target_components = (max(target_components, key=len),)
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
