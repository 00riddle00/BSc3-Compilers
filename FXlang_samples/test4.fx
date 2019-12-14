
fx main() ==> int {

   int a;
   int b = 8 * 25;

   int$ c;
   $c = 4;

    if (a < b) {
        return 1;
    } elif (a > b) {
        return 0;
    } else {
        return -1;
    }

    b = foo(14, 4*35) - 13;

    for (int i = 0; i < 10; ++i) {
          if (i > 0 AND True) {
              break;
          } else {
              continue;
          }
    }
}


fx foo(int c, int d) ==> int {
   return 0;
}
