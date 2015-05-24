package org.elsid.java_bytecode_model;

import org.elsid.java_bytecode_model.model.Model;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

class Main {

    public static void main(String[] args) {
        Model model = makeModel(args);
        System.out.print(model.toYaml());
    }

    static private Model makeModel(String[] paths) {
        ProjectFileVisitor visitor = new ProjectFileVisitor();
        ModelFactory factory = new ModelFactory();

        for (String path : paths) {
            try {
                Files.walkFileTree(Paths.get(path), visitor);
            } catch (IOException error) {
                System.err.format("Error when processing path '%s': %s\n", path, error.getMessage());
                error.printStackTrace();
            }

            visitor.getClasses().stream().forEach(factory::addClass);
            visitor.reset();
        }

        return factory.create();
    }

}
