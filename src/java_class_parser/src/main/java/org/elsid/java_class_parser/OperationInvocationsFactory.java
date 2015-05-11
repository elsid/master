package org.elsid.java_class_parser;

import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.EmptyVisitor;
import org.apache.bcel.generic.InvokeInstruction;
import org.elsid.java_class_parser.model.Classifier;
import org.elsid.java_class_parser.model.Operation;
import org.elsid.java_class_parser.model.Type;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

class OperationInvocationsFactory extends EmptyVisitor {

    private final TypesMap types;
    private final ConstantPoolGen constants;
    private final Operation operation;

    public OperationInvocationsFactory(TypesMap types, ConstantPoolGen constants, Operation operation) {
        this.types = types;
        this.constants = constants;
        this.operation = operation;
    }

    @Override
    public void visitInvokeInstruction(InvokeInstruction obj) {
        Classifier classifier = types.get(obj.getReferenceType(constants)).getClassifier();
        String name = obj.getMethodName(constants);
        Type result = types.get(obj.getReturnType(constants));
        List<Type> parametersTypes = Arrays.asList(obj.getArgumentTypes(constants))
            .stream().map(types::get).collect(Collectors.toList());
        Optional<Operation> invocation = classifier.getOperation(name, result, parametersTypes);
        if (invocation.isPresent()) {
            operation.addInvocation(invocation.get());
        }
    }

}
