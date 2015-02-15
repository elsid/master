#!/usr/bin/env python3
#coding: utf-8

from uml_matcher import (Aggregation, Class, Diagram, Operation, PrimitiveType,
    Property, Type, Interface)

INT_TYPE = PrimitiveType()

def create_decorator_pattern():
    component = Interface('Component',
        [],
        [Operation('operation')])
    concrete_component = Class('ConcreteComponent',
        [],
        [Operation('operation')])
    decorator_component = Property(Type(component), 'component')
    decorator = Interface('Decorator',
        [decorator_component],
        [Operation('operation')])
    concrete_decorator = Class('ConcreteDecorator',
        [],
        [Operation('operation')])
    return Diagram(
        generalizations=[
            (concrete_component, component),
            (decorator, component),
            (concrete_decorator, decorator),
        ],
        associations=[
            {decorator_component, Property(Type(decorator), 'decorator end 1', aggregation=Aggregation.shared)},
        ],
    )

def create_target_diagram():
    cutlet = Class('Cutlet',
        [],
        [Operation('price', result=Type(INT_TYPE))]
    )
    cheese = Class('Cheese',
        [],
        [Operation('price', result=Type(INT_TYPE))])
    burger = Class('Burger',
        [],
        [Operation('price', result=Type(INT_TYPE))])
    hamburger_cutlet = Property(Type(cutlet), 'cutlet')
    hamburger = Class('Hamburger',
        [hamburger_cutlet],
        [Operation('price', result=Type(INT_TYPE))])
    cheeseburger_cutlet = Property(Type(cutlet), 'cutlet')
    cheeseburger_cheese = Property(Type(cheese), 'cheese')
    cheeseburger = Class('Cheeseburger',
        [cheeseburger_cutlet, cheeseburger_cheese],
        [Operation('price', result=Type(INT_TYPE))])
    burger_with_burger = Property(Type(burger), 'burger')
    burger_with = Class('Burger with',
        [burger_with_burger],
        [Operation('price', result=Type(INT_TYPE))])
    return Diagram(
        generalizations=[
            (cutlet, burger_with),
            (cheese, burger_with),
            (burger_with, burger),
            (hamburger, burger),
            (cheeseburger, burger),
        ],
        associations=[
            {burger_with_burger, Property(Type(burger_with), 'burger_with end 1', aggregation=Aggregation.shared)},
            {hamburger_cutlet, Property(Type(hamburger), 'hamburger end 1', aggregation=Aggregation.shared)},
            {cheeseburger_cutlet, Property(Type(cheeseburger), 'cheeseburger end 1', aggregation=Aggregation.shared)},
            {cheeseburger_cheese, Property(Type(cheeseburger), 'cheeseburger end 2', aggregation=Aggregation.shared)},
        ],
    )

def print_graph_match_result(result):
    for index, variant in enumerate(result):
        print (index)
        for mapping in variant:
            print ('\t', mapping)

def print_uml_match_result(result):
    print_graph_match_result(result.generalizations)
    print_graph_match_result(result.associations)

if __name__ == '__main__':
    pattern = create_decorator_pattern()
    target = create_target_diagram()
    print (pattern)
    print (target)
    print_uml_match_result(target.match(pattern))
