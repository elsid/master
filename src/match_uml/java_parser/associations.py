# coding: utf-8

from uml_matcher import Class, Interface, Property, BinaryAssociation


def make_association(property_, types):
    return BinaryAssociation({
        property_,
        Property(types[property_.owner.name], property_.owner.name + '_end')})


def make_associations(types):
    associations = []
    for type_ in types.values():
        for property_ in type_.classifier.properties:
            if isinstance(property_.type.classifier, (Class, Interface)):
                associations.append(make_association(property_, types))
    return associations
