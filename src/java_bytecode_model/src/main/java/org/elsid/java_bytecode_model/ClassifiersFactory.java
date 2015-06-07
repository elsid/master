package org.elsid.java_bytecode_model;

import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.JavaClass;
import org.elsid.java_bytecode_model.model.Class;
import org.elsid.java_bytecode_model.model.Classifier;
import org.elsid.java_bytecode_model.model.Interface;

import java.util.ArrayList;
import java.util.Collection;

class ClassifiersFactory extends EmptyVisitor {

    private final Collection<Classifier> classifiers = new ArrayList<>();

    public void visitJavaClass(JavaClass obj) {
        if (obj.isInterface()) {
            classifiers.add(new Interface(obj.getClassName()));
        } else {
            classifiers.add(new Class(obj.getClassName()));
        }
    }

    public Collection<Classifier> get() {
        return classifiers;
    }

}
