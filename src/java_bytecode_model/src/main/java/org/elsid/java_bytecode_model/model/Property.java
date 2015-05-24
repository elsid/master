package org.elsid.java_bytecode_model.model;

import java.util.Map;

public class Property extends NamedElement {

    private Type type;
    private Visibility visibility;
    private Boolean isStatic;
    private Classifier owner;

    public void setType(Type type) {
        this.type = type;
    }

    public void setVisibility(Visibility visibility) {
        this.visibility = visibility;
    }

    public void setIsStatic(Boolean isStatic) {
        this.isStatic = isStatic;
    }

    public void setOwner(Classifier owner) {
        this.owner = owner;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("type", type);
        result.put("visibility", visibility);
        result.put("is_static", isStatic);
        result.put("owner", owner);
        return result;
    }

}
