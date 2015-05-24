package org.elsid.java_bytecode_model.model;

import java.util.HashMap;
import java.util.Map;

public class Type {

    private Classifier classifier;

    public Type(Classifier classifier) {
        this.classifier = classifier;
    }

    public Classifier getClassifier() {
        return classifier;
    }

    public Map<String, Object> toMap() {
        return new HashMap<String, Object>() {{
            put("classifier", classifier);
        }};
    }
}
