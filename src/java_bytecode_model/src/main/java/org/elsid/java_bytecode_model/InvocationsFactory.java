package org.elsid.java_bytecode_model;

import org.apache.bcel.classfile.Method;
import org.apache.bcel.generic.Visitor;

public class InvocationsFactory extends MethodInstructionsVisitor {

    public InvocationsFactory(TypesMap types) {
        super(types);
    }

    protected Visitor createFactory() {
        return new OperationInvocationsFactory(getTypes(), getConstants(), getOperation());
    }

    protected boolean needVisit(Method method) {
        return !method.getName().equals("<init>");
    }

}
