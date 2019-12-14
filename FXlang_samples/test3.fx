fx main() ==> int {

    int a;
    int b;
    int d = 1;
    int c = 2;

    if (a==c) {
        a %= ++d;
        return a+b*c;
    } elif (a == d) {
        return ++d;
    } else {
        return a+b*c;
    }
}
