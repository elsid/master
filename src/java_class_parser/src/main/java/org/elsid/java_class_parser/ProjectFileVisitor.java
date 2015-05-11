package org.elsid.java_class_parser;

import org.apache.bcel.classfile.ClassParser;
import org.apache.bcel.classfile.JavaClass;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Enumeration;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

class ProjectFileVisitor extends SimpleFileVisitor<Path> {

    private final Collection<JavaClass> classes = new ArrayList<>();

    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
        try {
            String filePath = file.toString();
            if (filePath.endsWith(".class")) {
                visitClassFile(filePath);
            } else if (filePath.endsWith(".jar")) {
                visitJarFile(filePath);
            }
        } catch (IOException error) {
            System.err.format("Error when processing sub path '%s': %s\n", file, error.getMessage());
            error.printStackTrace();
        }
        return FileVisitResult.CONTINUE;
    }

    void visitClassFile(String filePath) throws IOException {
        ClassParser parser = new ClassParser(filePath);
        classes.add(parser.parse());
    }

    void visitJarFile(String filePath) throws IOException {
        JarFile jar = new JarFile(filePath);
        Enumeration<JarEntry> entries = jar.entries();
        while (entries.hasMoreElements()) {
            JarEntry entry = entries.nextElement();
            if (!entry.isDirectory() && entry.getName().endsWith(".class")) {
                ClassParser parser = new ClassParser(filePath, entry.getName());
                classes.add(parser.parse());
            }
        }
    }

    public Collection<JavaClass> getClasses() {
        return classes;
    }

    public void reset() {
        classes.clear();
    }

}
