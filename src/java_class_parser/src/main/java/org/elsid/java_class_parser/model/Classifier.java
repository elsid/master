package org.elsid.java_class_parser.model;

import org.apache.bcel.classfile.Method;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public abstract class Classifier extends NamedElement {

    private final Collection<Property> properties = new ArrayList<>();
    private final Collection<Operation> operations = new ArrayList<>();
    private final Collection<Classifier> generals = new ArrayList<>();
    private final Collection<Classifier> suppliers = new HashSet<>();
    private final Map<Method, Operation> operationsTable = new HashMap<>();

    Classifier(String name) {
        super(name);
    }

    public void addProperty(Property property) {
        properties.add(property);
        property.setOwner(this);
    }

    public void addOperation(Method method, Operation operation) {
        operationsTable.put(method, operation);
        operations.add(operation);
        operation.setOwner(this);
    }

    public Operation getOperation(Method method) {
        return operationsTable.get(method);
    }

    public Optional<Operation> getOperation(String name, Type result, List<Type> parametersTypes) {
        return operations.stream().filter((operation) ->
                operation.getName().equals(name)
                    && operation.getResult().equals(result)
                    && operation.getParameters().stream().map(Parameter::getType)
                    .collect(Collectors.toList()).equals(parametersTypes)
        ).findAny();
    }

    public Optional<Operation> getOverriddenOperation(Operation overriding) {
        return operations.stream().filter((operation) -> operation.equals(overriding)).findAny();
    }

    public void addGeneral(Classifier general) {
        generals.add(general);
    }

    public void addSupplier(Classifier supplier) {
        suppliers.add(supplier);
    }

    public Map<String, Object> toMap() {
        Map<String, Object> result = super.toMap();
        result.put("properties", properties);
        result.put("operations", operations);
        result.put("generals", generals);
        result.put("suppliers", new ArrayList<>(suppliers));
        return result;
    }

}
