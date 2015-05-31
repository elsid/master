interface Interface {
    abstract void operation();
}

class Implementation implements Interface {
    public void operation() {}
}

class Client {
    Interface x = new Implementation();

    void invokeOperation() {
        x.operation();
    }
}
