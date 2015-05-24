package org.elsid.java_bytecode_model;

import org.apache.bcel.generic.Visitor;

public class DependenciesFactory extends MethodInstructionsVisitor {

    public DependenciesFactory(TypesMap types) {
        super(types);
    }

    protected Visitor createFactory() {
        return new OperationDependenciesFactory(getTypes(), getConstants(), getClassifier());
    }

}
