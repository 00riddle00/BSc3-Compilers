fx main() ==> int {

    int a = $$(a + 2);
    # int a = $a + 2;
    # foo($a + 2);
    # int a = ++(a + 2); # should not work
    # int a = a + 2; # should not work

}


#fx foo(int a) ==> int {
#   return 1;
#}