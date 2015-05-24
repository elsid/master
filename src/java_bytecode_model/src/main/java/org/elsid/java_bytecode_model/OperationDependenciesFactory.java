package org.elsid.java_bytecode_model;

import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.EmptyVisitor;
import org.apache.bcel.generic.TypedInstruction;
import org.elsid.java_bytecode_model.model.Classifier;
import org.elsid.java_bytecode_model.model.Type;

class OperationDependenciesFactory extends EmptyVisitor {

    private final TypesMap types;
    private final ConstantPoolGen constants;
    private final Classifier classifier;

    public OperationDependenciesFactory(TypesMap types, ConstantPoolGen constants, Classifier classifier) {
        this.types = types;
        this.constants = constants;
        this.classifier = classifier;
    }

    @Override
    public void visitTypedInstruction(TypedInstruction obj) {
        Type type = types.get(obj.getType(constants));
        classifier.addSupplier(type.getClassifier());
    }

}
