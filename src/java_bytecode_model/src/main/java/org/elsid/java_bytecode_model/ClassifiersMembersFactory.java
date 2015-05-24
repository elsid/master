package org.elsid.java_bytecode_model;


import org.apache.bcel.classfile.AccessFlags;
import org.apache.bcel.classfile.EmptyVisitor;
import org.apache.bcel.classfile.Field;
import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Method;
import org.elsid.java_bytecode_model.model.Classifier;
import org.elsid.java_bytecode_model.model.Direction;
import org.elsid.java_bytecode_model.model.Operation;
import org.elsid.java_bytecode_model.model.Parameter;
import org.elsid.java_bytecode_model.model.Property;
import org.elsid.java_bytecode_model.model.Visibility;

class ClassifiersMembersFactory extends EmptyVisitor {

    private final TypesMap types;
    private Classifier classifier;

    public ClassifiersMembersFactory(TypesMap types) {
        this.types = types;
    }

    private static Visibility getVisibility(AccessFlags accessFlags) {
        if (accessFlags.isPublic()) {
            return Visibility.PUBLIC;
        } else if (accessFlags.isProtected()) {
            return Visibility.PROTECTED;
        } else {
            return Visibility.PRIVATE;
        }
    }

    public void visitJavaClass(JavaClass obj) {
        classifier = types.getClassifiers().get(obj.getClassName());
        for (Field field : obj.getFields()) {
            field.accept(this);
        }
        for (Method method : obj.getMethods()) {
            method.accept(this);
        }
    }

    public void visitMethod(Method obj) {
        if (obj.getName().equals("<init>")) {
            return;
        }

        Operation operation = new Operation();
        operation.setName(obj.getName());
        operation.setResult(types.get(obj.getReturnType()));
        operation.setVisibility(getVisibility(obj));
        operation.setIsStatic(obj.isStatic());

        for (org.apache.bcel.generic.Type argumentType : obj.getArgumentTypes()) {
            Parameter parameter = new Parameter();
            parameter.setType(types.get(argumentType));
            parameter.setDirection(Direction.IN);
            operation.addParameter(parameter);
        }

        classifier.addOperation(obj, operation);
    }

    public void visitField(Field obj) {
        Property property = new Property();
        property.setName(obj.getName());
        property.setType(types.get(obj.getType()));
        property.setVisibility(getVisibility(obj));
        property.setIsStatic(obj.isStatic());
        classifier.addProperty(property);
    }

}
