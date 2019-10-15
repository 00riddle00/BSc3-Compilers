# this text is not very reada#@$%&\t\n##

int glob;

###
this comment spans

three lines \n \n \n \n \n \n \n
###

struct Test {
  int[4] list_of_ints;
  (char **)[] list_of_pointers_to_pointers_to_char;
}

fx get_all_atoms() => string {
  return "
    ! | # | @ | $ | % | & | ' | ( | ) | * | , | . | / | : |
    ; | < | = | > | ? | @ | [ | ] | ^ | ` | { | } | | | ~ |
    | _ | + | - | '' | \ | \" | \\ | (space) | \\n | \\r | \\t
    A | B | C | D | E | F | G | H | I | J | K | L | M | N |
    O | P | Q | R | S | T | U | V | W | X | Y | Z
    a | b | c | d | e | f | g | h | i | j | k | l | m | n |
    o | p | q | r | s | t | u | v | w | x | y | z
    0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
  "
}

fx print_info(int p, int q, char *separator) => void {

  string insight = "some r@ndom \"w\\sdom\"\0";

  if (p == 3 AND q != 2 OR p == 2 AND q > 0) {
    disp("Some insight->\t", insight, "\n");
  }
  elif(p < 3 OR p >= 5 OR q <= p) {
    disp(0, "ut", "of", "options");
  } else {
    disp("no result, hence no finish line");
    return;
  }

  # finish line
  disp(10*(*separator));
}

fx calc(int a, int b, float c, bool e) ==> int {
  int i;

  for (i = 0; i < 10;) {
    a /= b;

    if (c > a) {
      a *= 2;
    } else if (negative(a)) {
      break;
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

fx main() == > int {

  glob = -1;

  char *sep[2];

  *(sep[0]) = '\t';
  *(sep[1]) = '@';

  disp("Enter two numbers separated by comma > ");
  in(num1, "," num2);

  int N_1 = num1 %= num2;

  print_info(N_1, calc(N_1, -145, (+1.e10 - (-.3e-3) + glob), !(N_1 > 14)), sep[0]);

  glob = 1;

  return glob;

}