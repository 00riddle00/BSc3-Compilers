#include <stdio.h>

void main() {
    int* a;
    int *** c;
    **c = &*&a;
}
