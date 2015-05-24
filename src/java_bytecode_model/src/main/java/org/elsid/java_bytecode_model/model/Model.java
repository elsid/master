package org.elsid.java_bytecode_model.model;

import org.elsid.java_bytecode_model.model.yaml.ModelRepresenter;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.nodes.Tag;
import org.yaml.snakeyaml.representer.Representer;

import java.util.Collection;

public class Model {

    private final Collection<Classifier> classifiers;

    public Model(Collection<Classifier> classifiers) {
        this.classifiers = classifiers;
    }

    public String toYaml() {
        Representer representer = new ModelRepresenter();
        Yaml yaml = new Yaml(representer);
        return yaml.dumpAs(classifiers, new Tag("!Model"), null);
    }

}
