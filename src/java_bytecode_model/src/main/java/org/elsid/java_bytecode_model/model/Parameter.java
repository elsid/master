package org.elsid.java_bytecode_model.model;

import java.util.Map;

public class Parameter extends NamedElement {

    private Type type;
    private Direction direction;
    private int position;
    private Operation owner;

    public Type getType() {
        return type;
    }

    public void setType(Type type) {
        this.type = type;
    }

    public void setDirection(Direction direction) {
        this.direction = direction;
    }

    public void setPosition(int position) {
        this.position = position;
    }

    public void setOwner(Operation owner) {
        this.owner = owner;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("type", type);
        result.put("direction", direction);
        result.put("position", position);
        result.put("owner", owner);
        return result;
    }

}
