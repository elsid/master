# coding: utf-8

from copy import copy
from collections import namedtuple
from enum import Enum


class Equivalent(namedtuple('Equivalent', ('target', 'pattern'))):
    def __str__(self):
        return '%s === %s' % (self.target, self.pattern)

    def __repr__(self):
        return 'Equivalent(%s, %s)' % (repr(self.target), repr(self.pattern))


class EndType(Enum):
    INCOMING = 'incoming'
    OUTGOING = 'outgoing'

    def __str__(self):
        return self.value


class Configuration(object):
    def __init__(self, target_node, pattern_node, selected):
        e = Equivalent(target_node, pattern_node)
        self.__selected = [e] + selected
        self.__checked = {e}
        self.__current = 0

    def current(self):
        return self.__selected[self.__current]

    def target(self):
        return self.current().target

    def pattern(self):
        return self.current().pattern

    @property
    def selected(self):
        return self.__selected

    @property
    def checked(self):
        return self.__checked

    def checked_targets(self):
        return frozenset(x.target for x in self.__checked)

    def checked_patterns(self):
        return frozenset(x.pattern for x in self.__checked)

    def clone(self, additional_selected):
        other = copy(self)
        other.__selected = copy(self.__selected)
        other.__selected.extend(additional_selected)
        other.__checked = copy(self.__checked)
        return other

    def filter(self, pairs):
        return frozenset(pairs) - frozenset(self.__selected)

    def advance(self):
        checked_targets = self.checked_targets()
        checked_patterns = self.checked_patterns()

        def is_current_unchecked():
            return (self.target() not in checked_targets
                    and self.pattern() not in checked_patterns)

        def is_current_valid():
            target, pattern = self.current()

            def connections(neighbor, checked):
                for color, connection in checked.connections.iteritems():
                    if neighbor in connection.incoming:
                        yield (color, EndType.INCOMING)
                    if neighbor in connection.outgoing:
                        yield (color, EndType.OUTGOING)

            def is_valid(e):
                return (frozenset(connections(pattern, e.pattern))
                        <= frozenset(connections(target, e.target)))

            for x in self.__checked:
                if not is_valid(x):
                    return False
            return True

        while True:
            self.__current += 1
            if self.at_end():
                return
            if is_current_unchecked() and is_current_valid():
                self.__checked.add(self.current())
                return

    def at_end(self):
        return self.__current >= len(self.__selected)

    def __str__(self):

        def generate():
            for i, e in enumerate(self.__selected):
                if i == self.__current:
                    yield '[%s === %s]' % e
                elif e in self.__checked:
                    yield '{%s === %s}' % e
                elif i > self.__current:
                    yield '%s === %s' % e
                else:
                    yield '(%s === %s)' % e

        return ', '.join(generate())

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Configuration)
                and frozenset(self.__selected) == frozenset(other.selected))
