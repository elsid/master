package org.elsid.java_class_parser;

import org.apache.bcel.generic.Visitor;

public class InvocationsFactory extends MethodInstructionsVisitor {

    public InvocationsFactory(TypesMap types) {
        super(types);
    }

    protected Visitor createFactory() {
        return new OperationInvocationsFactory(getTypes(), getConstants(), getOperation());
    }

}