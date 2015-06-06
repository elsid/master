#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser, FileType
from sys import stdin
from match_pattern import load_model
from graph_matcher import count_arcs, count_connected_components


def main():
    args = parse_args()
    model = load_model(args.path)
    graph = model.graph()
    print 'nodes: %d' % len(graph.nodes)
    print 'arcs: %d' % count_arcs(graph)
    node = graph.least_connected_node()
    print 'least connected node: %s (%s)' % (node, node.count_connections())
    print ('connected components count: %s (%s)' %
           count_connected_components(graph))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('path', type=FileType('r'), nargs='?', default=stdin)
    return parser.parse_args()


if __name__ == '__main__':
    main()
