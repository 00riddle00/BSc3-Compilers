
fx main(int a, int b) ==> int {

   char z = 2;
   int$ c;
   c = &z;



   #int z = 2;
   #$c = 2;
   #c = &z;

    ###
    if (a+b+c) {
        return 8;
    }

    return (1 + 2) * b;
    ###
}
