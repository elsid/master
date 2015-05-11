package org.elsid.java_class_parser;

import org.apache.bcel.generic.Visitor;

public class DependenciesFactory extends MethodInstructionsVisitor {

    public DependenciesFactory(TypesMap types) {
        super(types);
    }

    protected Visitor createFactory() {
        return new OperationDependenciesFactory(getTypes(), getConstants(), getClassifier());
    }

}
