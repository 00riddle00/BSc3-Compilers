
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
    result: str

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.print_tokens()
        self.offset = 0
        self.result = ''

    def error(self):
        print('parse error')
        exit(1)

    def accept(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type == token_type:
            self.offset += 1
            return self.curr_token

    def expect(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type == token_type:
            self.offset += 1
            return self.curr_token
        else:
            print(f'syntax error in line {self.curr_token.line_no}')
            # todo add prety prints
            print(f'  expected={token_type}, found={self.curr_token.type}')
            exit(1)

    def parse_expr(self):
        self.parse_expr_add()

    # <ADD> ::= <MULT> | <ADD> "+" <MULT>
    # <ADD> ::= <MULT> {("+" | "-") <MULT>}
    def parse_expr_add(self):
        self.result = self.parse_expr_mult()

        while True:
            if self.accept('OP_SUM'):
                self.result = f'{self.result} ADD {self.parse_expr_mult()}'
            elif self.accept('OP_SUB'):
                self.result = f'{self.result} SUB {self.parse_expr_mult()}'
            else:
                break

        return self.result

    def parse_expr_lit_int(self):
        lit = self.expect('LIT_INT')
        self.result = 'LIT_INT'
        return self.result

    # <MULT> ::= <PRIMARY> | <MULT> "*" <PRIMARY>
    # <MULT> ::= <PRIMARY> {"*" <PRIMARY>}
    def parse_expr_mult(self):
        self.result = self.parse_expr_primary()

        while self.accept('OP_MULT'):
            self.result = 'MULT'

        return self.result

    # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
    def parse_expr_primary(self):
        if self.token_type() == 'IDENT':
            self.result = self.parse_expr_var()
        if self.token_type() == 'LIT_INT':
            self.result = self.parse_expr_lit_int()
        else:
            self.error()

        return self.result

    def parse_expr_var(self):
        name = self.expect('IDENT')
        self.result = 'IDENT'
        return self.result

    def token_type(self):
        return self.tokens[self.offset].type

    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.type},', end='')
        print('\n')



