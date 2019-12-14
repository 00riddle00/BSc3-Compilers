
fx test(int a, int b) ==> int {

    if (a+b > 0) {
        return 2;
    } elif (a-b > 0) {
        return 3;
    } elif (a*b > 0) {
        return 4;
    } else {
      b = ++a;
      return 5;
    }

    a += 2;
    int a;
    return 2;
}

fx main() ==> int {

    int c = 4;

    if (2 + 3 > 4) {
        return 8;
    }

    return (1 + 2) * c;
}
