from pprint import pprint

# <TERM> ::= <IDENT>
# <MULT> ::= <MULT> "*" <TERM> | <TERM>
# <ADD> ::= <ADD> "+" <MULT> | <MULT>

from lexer import Token

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
        return self.parse_expr_add()

    # <ADD> ::= <MULT> | <ADD> "+" <MULT>
    # <ADD> ::= <MULT> {("+" | "-") <MULT>}
    def parse_expr_add(self):
        self.result = self.parse_expr_mult()

        while True:
            if self.accept('OP_SUM'):
                self.result = ExprBinary('ADD', self.result, self.parse_expr_mult())
            elif self.accept('OP_SUB'):
                self.result = ExprBinary('SUB', self.result, self.parse_expr_mult())
            else:
                break

        return self.result

    def parse_expr_lit_int(self):
        lit = self.expect('LIT_INT')
        return ExprLit(lit)

    # <MULT> ::= <PRIMARY> | <MULT> "*" <PRIMARY>
    # <MULT> ::= <PRIMARY> {"*" <PRIMARY>}
    def parse_expr_mult(self):
        self.result = self.parse_expr_primary()

        while self.accept('OP_MULT'):
            self.result = ExprBinary('MULT', self.result, self.parse_expr_primary())

        return self.result

    # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
    def parse_expr_primary(self):
        if self.token_type() == 'IDENT':
            return self.parse_expr_var()
        if self.token_type() == 'LIT_INT':
            return self.parse_expr_lit_int()
        else:
            self.error()

    def parse_expr_var(self):
        name = self.expect('IDENT')
        return ExprVar(name)

    def token_type(self):
        return self.tokens[self.offset].type

    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.type},', end='')
        print('\n')


class Node(object):

    def __init__(self):
        pass

    def print_node(self, p):
        print(f'print not implemented for {self.__class__}')

class Expr(Node):

    def __init__(self):
        pass
        super().__init__()


class ExprBinary(Expr):

    # todo atr list everywhere

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        super().__init__()

    def print_node(self, p):
        p.print_single('op', self.op)
        p.print('left', self.left)
        p.print('right', self.right)


class ExprLit(Expr):

    def __init__(self, lit):
        self.lit = lit
        super().__init__()

    def print_node(self, p):
        p.print('lit', self.lit)


class ExprVar(Expr):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)


class ASTPrinter:

    def __init__(self):
        self.indent_level = 0

    def print(self, title, object):
        if isinstance(object, Node):
            self.print_node(title, object)
        elif isinstance(object, list):
            self.print_array(title, object)
        elif isinstance(object, Token):
            self.print_token(title, object)
        elif not object:
            self.print_single(title, 'NULL')
        else:
            # print(f'bad argument {object.__class__.__name__}')
            print(f'bad argument {object.__class__}')
            exit(1)

    def print_array(self, title, array):
        if not array:
            self.print_single(title, '[]')

        for ind, el in enumerate(array):
            print(f'{title}[{ind}], {el}')

    def print_node(self, title, node):
        self.print_single(title, f'{node.__class__}')
        self.indent_level += 1
        node.print_node(self)
        self.indent_level -= 1

    def print_single(self, title, text):
        prefix = '  ' * self.indent_level
        print(f'{prefix}{title}: {text}')

    def print_token(self, title, token):
        text = f'{token.value, token.line_no}'
        self.print_single(title, text)
