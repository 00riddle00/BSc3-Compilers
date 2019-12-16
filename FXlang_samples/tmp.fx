fx main() ==> int {
    int $a;
    int b = 2;
    $a = $foo(++b);
}
fx foo(int a) ==> int$ {
    return &a;
}