package org.elsid.java_class_parser;

import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Method;
import org.apache.bcel.generic.ConstantPoolGen;
import org.apache.bcel.generic.InstructionHandle;
import org.apache.bcel.generic.InstructionList;
import org.apache.bcel.generic.MethodGen;
import org.apache.bcel.generic.Visitor;
import org.elsid.java_class_parser.model.Classifier;
import org.elsid.java_class_parser.model.Operation;

abstract class MethodInstructionsVisitor extends EmptyVisitor {

    private final TypesMap types;
    private ConstantPoolGen constants;
    private Classifier classifier;
    private Operation operation;

    MethodInstructionsVisitor(TypesMap types) {
        this.types = types;
    }

    public void visitJavaClass(JavaClass obj) {
        classifier = types.getClassifiers().get(obj.getClassName());
        constants = new ConstantPoolGen(obj.getConstantPool());
        obj.getConstantPool().accept(this);
        for (Method method : obj.getMethods()) {
            method.accept(this);
        }
    }

    public void visitMethod(Method obj) {
        if (!needVisit(obj)) {
            return;
        }
        operation = classifier.getOperation(obj);
        MethodGen method = new MethodGen(obj, classifier.getName(), constants);
        InstructionList instructions = method.getInstructionList();
        if (instructions == null) {
            return;
        }
        Visitor factory = createFactory();
        for (InstructionHandle handle = instructions.getStart(); handle != null; handle = handle.getNext()) {
            handle.getInstruction().accept(factory);
        }
    }

    abstract protected Visitor createFactory();

    protected boolean needVisit(Method method) {
        return true;
    }

    TypesMap getTypes() {
        return types;
    }

    ConstantPoolGen getConstants() {
        return constants;
    }

    Classifier getClassifier() {
        return classifier;
    }

    Operation getOperation() {
        return operation;
    }

}
