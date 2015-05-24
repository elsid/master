package org.elsid.java_bytecode_model;

import org.elsid.java_bytecode_model.model.Classifier;
import org.elsid.java_bytecode_model.model.Type;

import java.util.HashMap;
import java.util.Map;

class TypesMap extends HashMap<org.apache.bcel.generic.Type, Type> {

    private final Map<String, Classifier> classifiers;

    public TypesMap(Map<String, Classifier> classifiers) {
        this.classifiers = classifiers;
    }

    @Override
    public Type get(Object key) {
        if (!containsKey(key)) {
            org.apache.bcel.generic.Type value = (org.apache.bcel.generic.Type) key;
            put(value, create(value));
        }
        return super.get(key);
    }

    public Map<String, Classifier> getClassifiers() {
        return classifiers;
    }

    Type create(org.apache.bcel.generic.Type value) {
        return new Type(classifiers.get(value.toString().replace("[]", "")));
    }

}
