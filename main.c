#include <stdio.h>

void main() {
    int a = 2;
    int* b;
    b = &&a;
    printf("%d\n", b);
    printf("%p\n", b);
}
