class SupplierLocalVariableType {}
class SupplierObjectConstructor {}

class Client {
    void operation() {
        SupplierLocalVariableType local;
        new SupplierObjectConstructor();
    }
}
