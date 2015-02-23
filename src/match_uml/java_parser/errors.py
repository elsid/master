# coding: utf-8


class Error(object):
    pass


class Redeclaration(Error):
    ENTITY = 'entity'

    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return 'redeclaration of {entity} "{name}"'.format(
            entity=self.ENTITY,
            name=self.declaration.name)

    def __repr__(self):
        return '"%s"' % str(self)

    def __eq__(self, other):
        return (self.ENTITY == other.ENTITY
                and self.declaration == other.declaration)


class ClassRedeclaration(Redeclaration):
    ENTITY = 'class'

    def __init__(self, declaration):
        super().__init__(declaration)


class InterfaceRedeclaration(Redeclaration):
    ENTITY = 'interface'

    def __init__(self, declaration):
        super().__init__(declaration)
