package org.elsid.java_class_parser.model.yaml;

import org.elsid.java_class_parser.model.Class;
import org.elsid.java_class_parser.model.DataType;
import org.elsid.java_class_parser.model.Direction;
import org.elsid.java_class_parser.model.Enumeration;
import org.elsid.java_class_parser.model.Interface;
import org.elsid.java_class_parser.model.Operation;
import org.elsid.java_class_parser.model.Parameter;
import org.elsid.java_class_parser.model.PrimitiveType;
import org.elsid.java_class_parser.model.Property;
import org.elsid.java_class_parser.model.Type;
import org.elsid.java_class_parser.model.Visibility;
import org.yaml.snakeyaml.nodes.Node;
import org.yaml.snakeyaml.nodes.Tag;
import org.yaml.snakeyaml.representer.Represent;
import org.yaml.snakeyaml.representer.Representer;

import java.util.Collection;
import java.util.Map;
import java.util.stream.Collectors;

public class ModelRepresenter extends Representer {

    public ModelRepresenter() {
        representers.put(Class.class, new ClassRepresent());
        representers.put(DataType.class, new DataTypeRepresent());
        representers.put(Enumeration.class, new EnumerationRepresent());
        representers.put(Interface.class, new InterfaceRepresent());
        representers.put(Operation.class, new OperationRepresent());
        representers.put(Parameter.class, new ParameterRepresent());
        representers.put(PrimitiveType.class, new PrimitiveTypeRepresent());
        representers.put(Property.class, new PropertyRepresent());
        representers.put(Type.class, new TypeRepresent());
        addClassTag(Direction.class, new Tag("!Direction"));
        addClassTag(Visibility.class, new Tag("!Visibility"));
    }

    private Map<String, Object> filter(Map<String, Object> map) {
        return map.entrySet().stream()
            .filter((entry) -> entry.getValue() != null)
            .filter((entry) -> !(entry.getValue() instanceof Collection)
                || !((Collection) entry.getValue()).isEmpty())
            .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }

    private class ClassRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Class"), filter(((Class) data).toMap()), null);
        }

    }

    private class DataTypeRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!DataType"), filter(((DataType) data).toMap()), null);
        }

    }

    private class EnumerationRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Enumeration"), filter(((Enumeration) data).toMap()), null);
        }

    }

    private class InterfaceRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Interface"), filter(((Interface) data).toMap()), null);
        }

    }

    private class OperationRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Operation"), filter(((Operation) data).toMap()), null);
        }

    }

    private class ParameterRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Parameter"), filter(((Parameter) data).toMap()), null);
        }

    }

    private class PrimitiveTypeRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!PrimitiveType"), filter(((PrimitiveType) data).toMap()), null);
        }

    }

    private class PropertyRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Property"), filter(((Property) data).toMap()), null);
        }

    }

    private class TypeRepresent implements Represent {

        public Node representData(Object data) {
            return representMapping(new Tag("!Type"), filter(((Type) data).toMap()), null);
        }

    }

}
