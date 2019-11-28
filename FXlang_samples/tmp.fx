
fx main(int a, int b) ==> int {

   int$ c;
   $c = 2;
   #int z = 2;
   #c = &z;

    ###
    if (a+b+c) {
        return 8;
    }

    return (1 + 2) * b;
    ###
}
