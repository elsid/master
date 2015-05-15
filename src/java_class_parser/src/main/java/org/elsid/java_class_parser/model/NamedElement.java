package org.elsid.java_class_parser.model;

import java.util.HashMap;
import java.util.Map;

public abstract class NamedElement {
    private String name;

    NamedElement() {
    }

    NamedElement(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    Map<String, Object> toMap() {
        return new HashMap<String, Object>() {{
            put("name", name);
        }};
    }

}
