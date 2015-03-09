# coding: utf-8

from collections import defaultdict, deque, Counter, namedtuple
from itertools import tee
from graph_matcher.configuration import Configuration


Equivalent = namedtuple('Equivalent', ('target', 'pattern'))


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
                    new_chain = list(chain) + [Equivalent(target, pattern)]
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


def match(target_graph, pattern_graph, limit=None):
    variants = deque()

    def init_generator():
        return generate_equivalent_node_pair(
            target_graph.nodes, pattern_graph.nodes, init_equivalent)

    for target_node, pattern_node in init_generator():
        conf = Configuration(target_node, pattern_node)
        variants.append(conf)
    result = []
    while variants:
        conf = variants.pop()
        if conf.at_end():
            if conf.visited_patterns() == pattern_graph.nodes:
                if conf.visited not in result:
                    result.append(conf.visited)
                    yield sorted(conf.visited)
                if limit is not None and len(result) >= limit:
                    return
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
                if 0 == target_equivalents[target_neighbor]:
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
