# coding: utf-8


class Element(object):
    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return hash(self) < hash(other)
