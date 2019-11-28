
###
this comment spans

three lines \n \n \n \n \n \n \n
###

fx get_all_atoms() ==> string {
  return "
    ! | # | @ | $ | % | & | ' | ( | ) | * | , | . | / | : |
    ; | < | = | > | ? | @ | [ | ] | ^ | ` | { | } | | | ~ |
    | _ | + | - | \" | \\ | (space) | \\n | \\r | \\t
    A | B | C | D | E | F | G | H | I | J | K | L | M | N |
    O | P | Q | R | S | T | U | V | W | X | Y | Z
    a | b | c | d | e | f | g | h | i | j | k | l | m | n |
    o | p | q | r | s | t | u | v | w | x | y | z
    0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
  ";
}

fx print_info(int p, int q, char separator) ==> void {

  string insight = "some r@ndom \"w\\sdom\"\"";

  if (p == 3 AND q != 2 OR p == 2 AND q > 0) {
    disp("Some insight->\t", insight, "\n");
  } elif(p < 3 OR p >= 5 OR q <= p) {
    disp(0, "ut", "of", "options");
  } else {
    disp("no result, hence no finish line");
    return;
  }

  # finish line
  disp(10*($separator));
}

fx calc(int a, int b, float c, bool e) ==> int {
  int i;

  for (i = 0; i < 10; ++i) {
    a /= b;

    if (c > a) {
      a *= 2;
    } elif (negative(a)) {
      return;
    }

    while (--a > 10) {
      ++b;
    }

    b -= 11;
    a += b;

    if (e AND c > 0) {
      a += 3;
    }

    ++i;
  }

  return a;
}

fx negative(int num) ==> bool {
  if (num > 0) {
    return False;
  } else {
    return True;
  }
}

fx main() ==> int {

  char$ sep;

  $(sep) = '\t';
  $(sep) = '@';

  int glob = 10;

  int num1;
  int num2;
  disp("Enter two numbers separated by comma > ");
  in(num1, ",", num2);

  int N_1 = num1 % num2;

  print_info(N_1, calc(N_1, -145, (+1.e10 - (.3e-3) + glob), !(N_1 > 14)), sep);

  glob = 1;

  return glob;

}