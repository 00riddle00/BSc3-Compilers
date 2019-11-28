fx main(int a, float b, int c) ==> void {
    ++(($a));
    ++($($($a)));
    $a = 2;
    $($$a) = 3;
    $a = $($foo(++b));
    $(a) = $($b) + ++c;
    $a = $(a+b);
    a = $(a+b);
    $(foo(123)) = 456;
    ++a = foo(bar(&b));
}

fx foo(int b) ==> int {
    return ++b;
}

fx bar(int p) ==> int {
    return ++p;
}
