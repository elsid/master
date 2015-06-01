class A {
    void invoked() {}

    void invoke() {
        invoked();
    }

    void invokeB() {
        new B().invoked();
    }
}

class B {
    void invoked() {}
}
