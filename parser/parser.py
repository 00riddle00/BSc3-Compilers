from pprint import pprint
from lexer import Token

# <TERM> ::= <IDENT>
# <MULT> ::= <MULT> "*" <TERM> | <TERM>
# <ADD> ::= <ADD> "+" <MULT> | <MULT>


class Parser:
    tokens: list
    offset: int
    curr_token: Token
    result: str

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.offset = 0
        self.result = ''

    def error(self, msg=''):
        print(f'parse error: {msg}')
        exit(1)

    def accept(self, token_type):
        # todo wrap into 'current' fn
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

    def parse_stmt_assign(self):
        var = self.expect('IDENT')
        self.expect('OP_ASSIGN_EQ')
        value = self.parse_expr()
        self.expect('OP_SEMICOLON')
        return StmtAssign(var, value)


    def parse_expr_call(self):
        name = self.expect('IDENT')
        args = []
        self.expect('OP_PAREN_O')

        if not self.peek('OP_PAREN_C'):
            args.append(self.parse_expr())

        while not self.peek('OP_PAREN_C'):
            self.expect('OP_COMMA')
            args.append(self.parse_expr())

        self.expect('OP_PAREN_C')
        return ExprCall(name, args)

    def parse_decl(self):
        return self.parse_decl_fn()

    def parse_decl_fn(self):
        self.expect('KW_FN')
        name = self.expect('IDENT')
        params = self.parse_params()
        self.expect('KW_FN_RET_ARROW')
        ret_type = self.parse_type()
        body = self.parse_stmt_block()
        return DeclFn(name, params, ret_type, body)

    # <EXPR> ::= <ADD>
    def parse_expr(self):
        return self.parse_expr_add()

    # <ADD> ::= <MULT> | <ADD> "+" <MULT>
    # <ADD> ::= <MULT> {("+" | "-") <MULT>}

    # older: <ADD> ::= <MULT> {OP_PLUS <MULT>}
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

    # older: <MULT> ::= <TERM> {OP_MULT <TERM>}
    def parse_expr_mult(self):
        self.result = self.parse_expr_primary()

        while self.accept('OP_MUL'):
            self.result = ExprBinary('MUL', self.result, self.parse_expr_primary())

        return self.result

    def parse_expr_paren(self):
        self.expect('OP_PAREN_O')
        self.result = self.parse_expr()
        self.expect('OP_PAREN_C')
        return self.result

    # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
    def parse_expr_primary(self):
        if self.peek2('IDENT', 'OP_PAREN_O'):
            return self.parse_expr_call()

        if self.token_type() == 'IDENT':
            return self.parse_expr_var()
        elif self.token_type() == 'LIT_INT':
            return self.parse_expr_lit_int()
        elif self.token_type() == 'OP_PAREN_O':
            return self.parse_expr_paren()
        else:
            self.error(f'expr error {self.curr_token}')

    def parse_expr_var(self):
        name = self.expect('IDENT')
        return ExprVar(name)

    def parse_param(self):
        type_ = self.parse_type()
        name = self.expect('IDENT')
        return Param(name, type_)

    def parse_params(self):
        params = []

        self.expect('OP_PAREN_O')

        if self.peek('OP_PAREN_C'):
            self.accept('OP_PAREN_C')
            return params
        else:
            params.append(self.parse_param())

        while not self.accept('OP_PAREN_C'):
            self.expect('OP_COMMA')
            params.append(self.parse_param())

        return params

    # <START> ::= {<DEF_FN>} EOF
    def parse_program(self):
        decls = []

        while True:
            if self.token_type() == 'EOF':
                break
            else:
                decls.append(self.parse_decl())

        return Program(decls)

    def parse_stmt(self):
        if self.peek2('IDENT', 'OP_ASSIGN_EQ'):
            return self.parse_stmt_assign()

        if self.token_type() == 'KW_IF':
            return self.parse_stmt_if()
        if self.token_type() == 'KW_WHILE':
            return self.parse_stmt_while()
        if self.token_type() == 'KW_BREAK':
            return self.parse_stmt_break()
        if self.token_type() == 'KW_RETURN':
            return self.parse_stmt_ret()
        else:
            self.error()

    def parse_stmt_block(self):
        self.expect('OP_BRACE_O')

        stmts = []

        while True:
            if self.accept('OP_BRACE_C'):
                break
            else:
                stmts.append(self.parse_stmt())
                pass

        return StmtBlock(stmts)

    def parse_stmt_if(self):
        self.expect('KW_IF')
        self.expect('OP_PAREN_O')
        cond = self.parse_expr()
        self.expect('OP_PAREN_C')
        body = self.parse_stmt_block()
        return StmtIf(cond, body)

    def parse_stmt_while(self):
        self.expect('KW_WHILE')
        self.expect('OP_PAREN_O')
        cond = self.parse_expr()
        self.expect('OP_PAREN_C')
        body = self.parse_stmt_block()
        return StmtWhile(cond, body)

    def parse_stmt_break(self):
        break_kw = self.expect('KW_BREAK')
        self.expect('OP_SEMICOLON')
        return StmtBreak(break_kw)

    def parse_stmt_ret(self):
        return_kw = self.expect('KW_RETURN')

        if self.token_type() != 'OP_SEMICOLON':
            value = self.parse_expr()
        else:
            value = None

        self.expect('OP_SEMICOLON')

        return StmtReturn(return_kw, value)

    def parse_type(self):
        if self.token_type() == 'KW_BOOL':
            self.expect('KW_BOOL')
            return TypePrim('BOOL')
        elif self.token_type() == 'KW_FLOAT':
            self.expect('KW_FLOAT')
            return TypePrim('FLOAT')
        elif self.token_type() == 'KW_INT':
            self.expect('KW_INT')
            return TypePrim('INT')
        elif self.token_type() == 'KW_VOID':
            self.expect('KW_VOID')
            return TypePrim('VOID')
        else:
            self.error()

    def peek(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type == token_type:
            return self.curr_token

    def peek2(self, token_type0, token_type1):
        token0 = self.tokens[self.offset + 0]
        token1 = self.tokens[self.offset + 1]
        return token0.type == token_type0 and token1.type == token_type1

    def token_type(self):
        return self.tokens[self.offset].type

    # fixme for debug
    def print_tokens(self):
        for token in self.tokens:
            print(f'{token.type},', end='')
        print('\n')

    def debug(self, msg):
        print(f'[debug:{msg}:{self.curr_token.type}:{self.curr_token.value}]')



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


class ExprCall(Expr):

    def __init__(self, name, args):
        self.name = name
        self.args = args
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('args', self.args)


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


class Param(Node):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)


class Program(Node):
    # std::vector<Decl*>
    def __init__(self, decls):
        self.decls = decls
        super().__init__()

    def print_node(self, p):
        p.print('decls', self.decls)


class Decl(Node):

    def __init__(self):
        pass
        super().__init__()


class DeclFn(Decl):

    def __init__(self, name, params, ret_type, body):
        self.name = name
        self.params = params
        self.ret_type = ret_type
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('params', self.params)
        p.print('ret_type', self.ret_type)
        p.print('body', self.body)


class Stmt(Node):

    def __init__(self):
        pass
        super().__init__()


class StmtBlock(Stmt):

    def __init__(self, stmts):
        self.stmts = stmts
        super().__init__()

    def print_node(self, p):
        p.print('stmts', self.stmts)


class StmtIf(Stmt):

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)


class StmtWhile(Stmt):

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)

class StmtBreak(Stmt):

    def __init__(self, break_kw):
        self.break_kw = break_kw
        super().__init__()

    def print_node(self, p):
        p.print('break_kw', self.break_kw)

class StmtReturn(Stmt):

    def __init__(self, return_kw, value):
        self.return_kw = return_kw
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('return_kw', self.return_kw)
        p.print('value', self.value)

class StmtAssign(Stmt):

    def __init__(self, var, value):
        self.var = var
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('var', self.var)
        p.print('value', self.value)


class Type(Node):

    def __init__(self):
        pass
        super().__init__()


class TypePrim(Type):

    def __init__(self, kind):
        self.kind = kind
        super().__init__()

    def print_node(self, p):
        p.print_single('kind', self.kind)


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
            print(f'bad argument {object.__class__.__name__}')
            # print(f'bad argument {object.__class__}')
            exit(1)

    def print_array(self, title, array):
        if not array:
            self.print_single(title, '[]')

        for ind, el in enumerate(array):
            # print(f'{title}[{ind}], {el}')
            self.print(f'{title}[{ind}]', el)

    def print_node(self, title, node):
        self.print_single(title, f'{node.__class__.__name__}:')
        self.indent_level += 1
        node.print_node(self)
        self.indent_level -= 1

    def print_single(self, title, text):
        prefix = '  ' * self.indent_level
        print(f'{prefix}{title}: {text}')

    def print_token(self, title, token):
        text = f'{token.value} (ln={token.line_no})'
        self.print_single(title, text)

