package org.elsid.java_class_parser.model;

import java.util.Map;

public class Property extends NamedElement {

    private Type type;
    private Visibility visibility;
    private Boolean isStatic;

    public void setType(Type type) {
        this.type = type;
    }

    public void setVisibility(Visibility visibility) {
        this.visibility = visibility;
    }

    public void setIsStatic(Boolean isStatic) {
        this.isStatic = isStatic;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("type", type);
        result.put("visibility", visibility);
        result.put("is_static", isStatic);
        return result;
    }

}
