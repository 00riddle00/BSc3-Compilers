
    if (5 - -e AND foo((c > 0 + False))) {
         a += 3;
    } elif (x) { 
        
    }
        
```
<STMT> =>
<IF_STMT> =>
<IF_IF> <IF_ELIFS> =>
"if" "(" <EXPR> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <OR> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <AND> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <AND> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <CMP_EQ_NEQ> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <CMP_GT_LT> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <SUM_SUB> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <SUM_SUB> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <MUL_DIV_MOD> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <UNARY> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <PRIMARY> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <BASE_TYPE_LIT> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <INT_LIT> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <SIGNABLE_DIGITS> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <DIGITS><OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" <DIGIT> <OP_SUM_SUB> <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" <MUL_DIV_MOD> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" <UNARY> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" <OP_UNARY> <UNARY> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" <SIGN> <UNARY> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <UNARY> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <PRIMARY> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <VAR> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <IDENT> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <IDENT_HEAD_SYM> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <LETTER> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" <LCASE_LETTER> <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" <OP_AND> <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <CMP_EQ_NEQ> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <CMP_GT_LT> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <SUM_SUB> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <MUL_DIV_MOD> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <UNARY> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <PRIMARY> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <FN_CALL> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <IDENT> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <IDENT> <IDENT_TAIL_SYM> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <IDENT> <IDENT_TAIL_SYM> <IDENT_TAIL_SYM> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <IDENT_HEAD_SYM> <IDENT_TAIL_SYM> <IDENT_TAIL_SYM> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" <IDENT_HEAD_SYM> <IDENT_HEAD_SYM> <IDENT_HEAD_SYM> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" <LETTER> <LETTER> <LETTER> <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" <ARGS> ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" <ARGS_SEQ> ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" <ARG> ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" <EXPR> ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" <PRIMARY> ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <EXPR> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <AND> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <CMP_EQ_NEQ> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <CMP_GT_LT> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <CMP_GT_LT> <OP_CMP_GT_LT> <SUM_SUB> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" <LETTER> <OP_CMP_GT_LT> <SUM_SUB> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" <OP_CMP_GT_LT> <SUM_SUB> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" <SUM_SUB> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" <SUM_SUB> <OP_SUM_SUB> <MUL_DIV_MOD> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" <DIGIT> <OP_SUM_SUB> <MUL_DIV_MOD> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" <OP_SUM_SUB> <MUL_DIV_MOD> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" <MUL_DIV_MOD> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" <PRIMARY> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" <BASE_TYPE_LIT> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" <BOOL_LIT> ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" <STMT_BLOCK> <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <STMTS> "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <STMT> "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <STATEMENT_W_DELIM> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <ASSIGNMENT_STMT> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <ASSIGNMENT> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <LVALUE> <OP_ASSIGN> <EXPR> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <VAR_LVALUE> <OP_ASSIGN> <EXPR> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <IDENT> <OP_ASSIGN> <EXPR> ";" "}" <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" <LETTER> <OP_ASSIGN> <EXPR> ";" "}" <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" <OP_ASSIGN> <EXPR> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" <EXPR> ";" "}" <IF_ELIFS> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" <DIGIT> ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" <IF_ELIFS> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" <IF_ELIF> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" "elif" "(" <EXPR> ")" <STMT_BLOCK> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" "elif" "(" <LETTER> ")" <STMT_BLOCK> =>
...
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" "elif" "(" "x" ")" <STMT_BLOCK> =>
"if" "(" "5" "-" "-" "e" "AND" "f" "o" "o" "(" "(" "c" ">" "0" "+" "False" ")" ")" ")" "{" "a" "+=" "3" ";" "}" "elif" "(" "x" ")" "{" "}"
```

