
# <TERM> ::= <IDENT>
# <MULT> ::= <MULT> "*" <TERM> | <TERM>
# <ADD> ::= <ADD> "+" <MULT> | <MULT>


class Token:
    type_: str
    value: str
    line_no: int

    def __init__(self, type_, value, line_no):
        self.type = type_
        self.value = value
        self.line_no = line_no


class Parser:
    tokens: list
    offset: int
    curr_token: Token

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.print_tokens()
        self.offset = 0

    def error(self):
        print('parse error')
        exit(1)

    def accept(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type_ == token_type:
            self.offset += 1
            return self.curr_token

    def expect(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type_ == token_type:
            self.offset += 1
            return self.curr_token
        else:
            print(f'syntax error in line {self.curr_token.line_no}')
            # todo add prety prints
            print(f'  expected={token_type}, found={self.curr_token.type_}')
            exit(1)

    def parse_expr(self):
        self.parse_expr_add()

    # <ADD> ::= <MULT> | <ADD> "+" <MULT>
    # <ADD> ::= <MULT> {("+" | "-") <MULT>}
    def parse_expr_add(self):
        self.result = self.parse_expr_mult()
        print("MULT done")

        while True:
            if self.accept('OP_PLUS'):
                self.result = 'ADD'
            elif self.accept('OP_MINUS'):
                self.result = 'SUB'
            else:
                break

        return self.result

    def parse_expr_lit_int(self):
        lit = self.expect('LIT_INT')

    # <MULT> ::= <PRIMARY> | <MULT> "*" <PRIMARY>
    # <MULT> ::= <PRIMARY> {"*" <PRIMARY>}
    def parse_expr_mult(self):
        self.parse_expr_primary()
        print("PRIM done")

        while self.accept('OP_MULT'):
            self.result = 'MULT'

        return self.result

    # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
    def parse_expr_primary(self):
        if self.token_type() == 'IDENT':
            self.parse_expr_var()
        if self.token_type() == 'LIT_INT':
            self.parse_expr_lit_int()
        else:
            self.error()

    def parse_expr_var(self):
        name = self.expect('IDENT')

    def token_type(self):
        return self.tokens[self.offset].type_

    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.type},', end='')
        print('\n')



