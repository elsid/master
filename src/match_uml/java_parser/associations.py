# coding: utf-8

from uml_matcher import Class, Interface, Property, BinaryAssociation


def make_associations(types):
    associations = []
    for type_ in types.values():
        for property_ in type_.classifier.properties:
            if isinstance(property_.type.classifier, (Class, Interface)):
                end_type = types[property_.owner.name]
                end = Property(end_type, property_.owner.name + '_end')
                associations.append(BinaryAssociation({property_, end}))
                property_.associations.append(end)
                end.associations.append(property_)
    return associations
