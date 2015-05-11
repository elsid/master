package org.elsid.java_class_parser;

import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.JavaClass;
import org.elsid.java_class_parser.model.Class;
import org.elsid.java_class_parser.model.Classifier;
import org.elsid.java_class_parser.model.Enumeration;
import org.elsid.java_class_parser.model.Interface;

import java.util.ArrayList;
import java.util.Collection;

class ClassifiersFactory extends EmptyVisitor {

    private final Collection<Classifier> classifiers = new ArrayList<>();

    public void visitJavaClass(JavaClass obj) {
        if (obj.isEnum()) {
            classifiers.add(new Enumeration(obj.getClassName()));
        } else if (obj.isInterface()) {
            classifiers.add(new Interface(obj.getClassName()));
        } else {
            classifiers.add(new Class(obj.getClassName()));
        }
    }

    public Collection<Classifier> get() {
        return classifiers;
    }

}
