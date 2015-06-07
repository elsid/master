package org.elsid.java_bytecode_model;

import org.elsid.java_bytecode_model.model.Classifier;
import org.elsid.java_bytecode_model.model.PrimitiveType;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;

class ClassifiersMap extends HashMap<String, Classifier> {

    static final private Collection<String> PRIMITIVE_TYPES = new HashSet<>(Arrays.asList(
        "void", "byte", "short", "int", "long", "float", "double", "boolean", "char"));

    @Override
    public Classifier get(Object key) {
        if (!containsKey(key)) {
            String name = (String) key;
            put(name, create(name));
        }
        return super.get(key);
    }

    Classifier create(String name) {
        if (PRIMITIVE_TYPES.contains(name)) {
            return new PrimitiveType(name);
        } else {
            return new Classifier(name);
        }
    }

}
