
fx main() ==> void {

    ++((a));
    ++(*(*(*a)));
    a = 1;
    *a = 2;
    *(**a) = 3;

    if (a+b) {
        a %= ++d;
        return a+b*c;
    } else {
        return a+b*c;
    }
}
