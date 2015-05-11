package org.elsid.java_class_parser.model;

import java.util.Map;

public class Parameter extends NamedElement {

    private Type type;
    private Direction direction;

    public Type getType() {
        return type;
    }

    public void setType(Type type) {
        this.type = type;
    }

    public void setDirection(Direction direction) {
        this.direction = direction;
    }

    public boolean equals(Object other) {
        return other instanceof Parameter
            && type == ((Parameter) other).type
            && direction == ((Parameter) other).direction;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("type", type);
        result.put("direction", direction);
        return result;
    }
}
