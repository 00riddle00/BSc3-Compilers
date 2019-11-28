fx test(int a, int b) ==> void {

    if (a+b) {
        return 2;
    } elif (a-b) {
        return 3;
    } elif (a*b) {
        return 4;
    } else {
      b = ++a;
      return 5;
    }

    a += 2;
    int a;
    return 2;
}

fx main(int a, float b) ==> int {

    if (a+b) {
        return 8;
    }

    return (1 + 2) * b;
}
