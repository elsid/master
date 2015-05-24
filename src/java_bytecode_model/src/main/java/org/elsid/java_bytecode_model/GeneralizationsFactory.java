package org.elsid.java_bytecode_model;

import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.JavaClass;
import org.elsid.java_bytecode_model.model.Classifier;

import java.util.Map;

class GeneralizationsFactory extends EmptyVisitor {

    private final Map<String, Classifier> classifiers;

    public GeneralizationsFactory(Map<String, Classifier> classifiers) {
        this.classifiers = classifiers;
    }

    public void visitJavaClass(JavaClass obj) {
        Classifier classifier = classifiers.get(obj.getClassName());
        if (!"java.lang.Object".equals(obj.getSuperclassName())) {
            classifier.addGeneral(classifiers.get(obj.getSuperclassName()));
        }
        for (String general : obj.getInterfaceNames()) {
            if (!"java.lang.Object".equals(general)) {
                classifier.addGeneral(classifiers.get(general));
            }
        }
    }

}
