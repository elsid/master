package org.elsid.java_class_parser.model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

public class Operation extends NamedElement {

    private final List<Parameter> parameters = new ArrayList<>();
    private final Collection<Operation> invocations = new HashSet<>();
    private Type result;
    private Visibility visibility;
    private Boolean isStatic;

    public Type getResult() {
        return result;
    }

    public void setResult(Type result) {
        this.result = result;
    }

    public void setVisibility(Visibility visibility) {
        this.visibility = visibility;
    }

    public List<Parameter> getParameters() {
        return Collections.unmodifiableList(parameters);
    }

    public void addParameter(Parameter parameter) {
        parameters.add(parameter);
    }

    public void setIsStatic(Boolean isStatic) {
        this.isStatic = isStatic;
    }

    public void addInvocation(Operation invoked) {
        invocations.add(invoked);
    }


    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("result", this.result);
        result.put("visibility", visibility);
        result.put("parameters", parameters);
        result.put("is_static", isStatic);
        result.put("invocations", new ArrayList<>(invocations));
        return result;
    }

}
