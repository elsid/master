# coding: utf-8

from collections import defaultdict, deque, Counter, namedtuple
from itertools import tee, combinations, permutations
from graph_matcher.configuration import Configuration


Equivalent = namedtuple('Equivalent', ('target', 'pattern'))


def replace_node_by_obj(variants):
    return [[Equivalent(x.target.obj, x.pattern.obj) for x in variant]
            for variant in variants]


def generate_equivalent_node_pair(target_nodes, pattern_nodes, equivalent):
    for target_node in target_nodes:
        for pattern_node in pattern_nodes:
            if equivalent(target_node, pattern_node):
                yield target_node, pattern_node


def make_equivalent_node_pairs_generator(target_nodes, pattern_nodes,
                                         equivalent):
    def generate_pairs():
        return generate_equivalent_node_pair(target_nodes, pattern_nodes,
                                             equivalent)

    def generate():
        pattern_dict = defaultdict(set)
        for target, pattern in generate_pairs():
            pattern_dict[pattern].add(target)

        def gen_recursive(pattern_iter, chain=tuple()):
            try:
                pattern = next(pattern_iter)
                not_used_targets = list(pattern_dict[pattern].difference(
                    set((target for target, _ in chain))))
                pattern_iters = tee(pattern_iter, len(not_used_targets))
                for index, target in enumerate(not_used_targets):
                    new_chain = list(chain) + [(target, pattern)]
                    for c in gen_recursive(pattern_iters[index], new_chain):
                        yield c
            except StopIteration:
                yield chain

        for chain in gen_recursive(iter(sorted(pattern_dict.keys()))):
            yield chain

    return generate


def init_equivalent(target, pattern):
    return target.equiv_pattern(pattern)


def remove_duplicates(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def match_one(target_graph, pattern_graph):
    def init_generator():
        return generate_equivalent_node_pair(
            target_graph.nodes, pattern_graph.nodes, init_equivalent)

    variants = deque(Configuration(target_node, pattern_node)
                     for target_node, pattern_node in init_generator())
    result = []
    while variants:
        conf = variants.pop()
        if conf.at_end():
            if conf.visited_patterns() == pattern_graph.nodes:
                if conf.visited not in result:
                    result.append(conf.visited)
                    yield sorted(Equivalent(t, p) for t, p in conf.visited)
            continue

        def neighbor_equivalent(target_node, pattern_node):
            return ((target_node, pattern_node) in conf.visited
                    or init_equivalent(target_node, pattern_node))

        def current_equivalent(target_node, pattern_node):
            if not init_equivalent(target_node, pattern_node):
                return False
            target_equivalents = Counter()
            for target_neighbor in target_node.neighbors():
                for pattern_neighbor in pattern_node.neighbors():
                    if neighbor_equivalent(target_neighbor, pattern_neighbor):
                        target_equivalents[target_neighbor] += 1
            for target_neighbor in target_node.neighbors():
                if target_equivalents[target_neighbor] == 0:
                    return False
            return True

        variants_generator = make_equivalent_node_pairs_generator(
            conf.target().neighbors(), conf.pattern().neighbors(),
            current_equivalent)
        repush = True
        for pairs in variants_generator():
            pairs = conf.filter(pairs)
            if pairs:
                new_conf = conf.copy()
                new_conf.extend(pairs)
                if set(new_conf.selected) not in result:
                    new_conf.step()
                    variants.append(new_conf)
                    repush = False
        if repush:
            conf.step()
            variants.append(conf)


def match_one_pattern(pattern_graph, target_components):
    from graph_matcher.graph import Graph
    for component in target_components:
        for v in match_one(Graph(nodes=component), pattern_graph):
            yield v


def match_one_target(target_graph, pattern_components):
    from graph_matcher.graph import Graph
    for component in pattern_components:
        for v in match_one(target_graph, Graph(nodes=component)):
            yield v


def match(target_graph, pattern_graph):
    from graph_matcher.graph import Graph
    target_components = tuple(target_graph.get_connected_components())
    pattern_components = tuple(pattern_graph.get_connected_components())
    target_n = len(target_components)
    pattern_n = len(pattern_components)
    if target_n <= 1:
        if pattern_n <= 1:
            for v in match_one(target_graph, pattern_graph):
                yield v
        else:
            for v in match_one_target(target_graph, pattern_components):
                yield v
    else:
        if pattern_n <= 1:
            for v in match_one_pattern(pattern_graph, target_components):
                yield v
        else:
            if pattern_n < target_n:

                def match_combination(target_components):
                    for target_component in target_components:
                        target_graph = Graph(nodes=target_component)
                        for pp in permutations(pattern_components, pattern_n):
                            for v in match_one_target(target_graph, pp):
                                yield v

                target_combinations = combinations(target_components, pattern_n)
                for target_combination in target_combinations:
                    variants = generate_merged_variants(match_combination(
                        target_combination))
                    for v in variants:
                        yield v
            else:

                def match_combination(pattern_components):
                    for pattern_component in pattern_components:
                        pattern_graph = Graph(nodes=pattern_component)
                        for tp in permutations(target_components, target_n):
                            for v in match_one_pattern(pattern_graph, tp):
                                yield v

                pattern_combinations = combinations(pattern_components,
                                                    target_n)
                for pattern_combination in pattern_combinations:
                    variants = generate_merged_variants(match_combination(
                        pattern_combination))
                    for v in variants:
                        yield v


def generate_merged_variants(variants):
    variants = tuple(variants)
    for n in xrange(len(variants), 0, -1):
        result = []
        for combination in combinations(variants, n):
            union = unite_variants(combination)
            if union:
                union = sorted(union)
                if union not in result:
                    result.append(union)
                    yield union
        if result:
            return


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
