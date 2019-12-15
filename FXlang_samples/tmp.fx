fx main() ==> int {

    int $a;
    ++($($($a))); # should not work

}


fx foo(int a) ==> int {
   return 1;
}