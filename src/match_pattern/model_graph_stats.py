#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser, FileType
from sys import stdin
from match_pattern import load_model


def main():
    args = parse_args()
    model = load_model(args.path)
    graph = model.graph()
    print 'nodes: %d' % len(graph.nodes)
    print 'arcs: %d' % arcs(graph.nodes)
    node = graph.least_connected_node()
    print 'least connected node: %s (%s)' % (node, node.count_connections())
    components = tuple(graph.get_connected_components())
    print ('connected components count: %s (%s)' %
           (len(components), ', '.join(str(len(x)) for x in components)))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('path', type=FileType('r'), nargs='?', default=stdin)
    return parser.parse_args()


def arcs(nodes):
    return sum(sum(len(x.incoming) + len(x.outgoing)
                   for x in n.connections.values()) for n in nodes)


if __name__ == '__main__':
    main()
