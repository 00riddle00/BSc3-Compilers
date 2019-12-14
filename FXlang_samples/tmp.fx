fx main(int a, int b) ==> void {

    $($(a)) = ++b;
    int d = 1;
    int c = 2;

    if (a==c) {
        a %= ++d;
        return a+b*c;
    } elif (a == d) {
        return a+b*c;
    } else {
        return a+b*c;
    }
}
