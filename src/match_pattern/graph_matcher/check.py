# coding: utf-8

from collections import namedtuple
from graph_matcher.configuration import EndType, Isomorphic
from graph_matcher.match import replace_node_by_obj


Connection = namedtuple('Connection', ('label', 'end_type', 'node'))


class CheckIsomorphismFailed(Exception):
    def __init__(self, isomorphism, wrong_isomorphic, connection):
        super(CheckIsomorphismFailed, self).__init__()
        self.isomorphism = isomorphism
        self.wrong_isomorphic = wrong_isomorphic
        self.connection = connection

    def __str__(self):

        def generate():
            for i in self.isomorphism:
                base = '%s === %s' % (repr(i.target), repr(i.pattern))
                label = self.connection.label.__name__
                end_type = self.connection.end_type
                if i == self.wrong_isomorphic:
                    yield '  %s <<< %s (%s)' % (base, label, end_type)
                else:
                    yield '  ' + base

        return 'check isomorphism failed\n%s' % '\n'.join(generate())

    def __repr__(self):
        return 'CheckIsomorphismFailed(%s, %s, %s)' % tuple(repr(x) for x in (
            self.isomorphism, self.wrong_isomorphic, self.connection))


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
                            i = Isomorphic(isomorphic.target.obj,
                                           isomorphic.pattern.obj)
                            raise CheckIsomorphismFailed(
                                replace_node_by_obj(isomorphism), i, connection)
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
