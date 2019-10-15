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

struct Test *test_struct;

(*test_struct).list_of_ints = [[1,2],[3,4]];
