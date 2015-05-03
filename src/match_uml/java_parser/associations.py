# coding: utf-8

from uml_matcher import Class, Interface, Property


class MakeAssociations(object):
    def __init__(self, types):
        self.types = types
        self.__ends = {}

    def generate(self):
        for type_ in self.types.values():
            for property_ in type_.classifier.properties:
                property_classifier = property_.type.classifier
                if isinstance(property_classifier, (Class, Interface)):
                    end = self.__get_end(property_.owner.name)
                    property_.associations.append(end)
                    end.associations.append(property_)

    def __get_end(self, classifier_name):
        end_name = classifier_name + '_end'
        if end_name in self.__ends:
            return self.__ends[end_name]
        end_type = self.types[classifier_name]
        end = Property(end_type, end_name)
        self.__ends[end_name] = end
        return end


def make_associations(types):
    factory = MakeAssociations(types)
    factory.generate()
