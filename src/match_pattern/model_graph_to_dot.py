#!/usr/bin/env python
# coding: utf-8

from match_pattern import load_model
from model_graph_stats import parse_args


def main():
    args = parse_args()
    model = load_model(args.path)
    graph = model.graph()
    print graph.as_dot().to_string()


if __name__ == '__main__':
    main()
