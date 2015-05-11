package org.elsid.java_class_parser;

import org.apache.bcel.classfile.JavaClass;
import org.apache.bcel.classfile.Visitor;
import org.elsid.java_class_parser.model.Classifier;
import org.elsid.java_class_parser.model.Model;
import org.elsid.java_class_parser.model.Operation;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Optional;

class ModelFactory {

    private final Collection<JavaClass> javaClasses = new ArrayList<>();
    private final ClassifiersMap classifiers = new ClassifiersMap();
    private TypesMap types;

    public void addClass(JavaClass javaClass) {
        javaClasses.add(javaClass);
    }

    public Model create() {
        makeClassifiers();
        makeGeneralizations();
        makeTypes();
        fillClassifiersMembers();
        makeDependencies();
        makeInvocations();
        makeOverriding();
        return new Model(new ArrayList<>(classifiers.values()));
    }

    void makeClassifiers() {
        ClassifiersFactory factory = new ClassifiersFactory();
        for (JavaClass javaClass : javaClasses) {
            javaClass.accept(factory);
        }
        for (Classifier classifier : factory.get()) {
            classifiers.put(classifier.getName(), classifier);
        }
    }

    void makeGeneralizations() {
        Visitor factory = new GeneralizationsFactory(classifiers);
        for (JavaClass javaClass : javaClasses) {
            javaClass.accept(factory);
        }
    }

    void makeTypes() {
        types = new TypesMap(classifiers);
    }

    void fillClassifiersMembers() {
        Visitor factory = new ClassifiersMembersFactory(types);
        for (JavaClass javaClass : javaClasses) {
            javaClass.accept(factory);
        }
    }

    void makeDependencies() {
        Visitor factory = new DependenciesFactory(types);
        for (JavaClass javaClass : javaClasses) {
            javaClass.accept(factory);
        }
    }

    void makeInvocations() {
        Visitor factory = new InvocationsFactory(types);
        for (JavaClass javaClass : javaClasses) {
            javaClass.accept(factory);
        }
    }

    void makeOverriding() {
        for (Classifier classifier : classifiers.values()) {
            classifier.getOperations().forEach(
                (operation) -> {
                    for (Classifier general : classifier.getGenerals()) {
                        Optional<Operation> overridden = general.getOverriddenOperation(operation);
                        if (overridden.isPresent()) {
                            operation.setOverridden(overridden.get());
                            return;
                        }
                    }
                }
            );
        }
    }

}
