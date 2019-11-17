from pprint import pprint
from lexer import Token
import inspect

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
        # todo do not allow var to be keyword (ex TRUE, NULL)
        var = self.expect('IDENT')

        if self.token_type() == 'OP_ASSIGN_EQ':
            self.expect('OP_ASSIGN_EQ')
            op = 'EQUALS'
        elif self.token_type() == 'OP_ASSIGN_SUM':
            self.expect('OP_ASSIGN_SUM')
            op = 'PLUS_EQUALS'
        elif self.token_type() == 'OP_ASSIGN_SUB':
            self.expect('OP_ASSIGN_SUB')
            op = 'MINUS_EQUALS'
        elif self.token_type() == 'OP_ASSIGN_MUL':
            self.expect('OP_ASSIGN_MUL')
            op = 'MULT_EQUALS'
        elif self.token_type() == 'OP_ASSIGN_DIV':
            self.expect('OP_ASSIGN_DIV')
            op = 'DIV_EQUALS'
        elif self.token_type() == 'OP_ASSIGN_MOD':
            self.expect('OP_ASSIGN_MOD')
            op = 'MOD_EQUALS'
        else:
            self.error('invalid assign op')

        value = self.parse_expr()
        self.expect('OP_SEMICOLON')
        return StmtAssign(var, op, value)

    def parse_stmt_expr(self, expr):
        self.result = expr
        self.expect('OP_SEMICOLON')
        return StmtExpr(self.result)

    def parse_expr_fn_call(self):
        name = self.expect('IDENT')
        args = []
        self.expect('OP_PAREN_O')

        if not self.peek('OP_PAREN_C'):
            args.append(self.parse_expr())

        while not self.peek('OP_PAREN_C'):
            self.expect('OP_COMMA')
            args.append(self.parse_expr())

        self.expect('OP_PAREN_C')
        return ExprFnCall(name, args)

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
        return self.parse_expr_or()

    def parse_expr_or(self):
        self.result = self.parse_expr_and()

        while True:
            if self.accept('KW_OR'):
                self.result = ExprBinary('logical_or', 'OR', self.result, self.parse_expr_and())
            else:
                break

        return self.result

    def parse_expr_and(self):
        self.result = self.parse_expr_cmp()

        # todo remove useless while
        while True:
            if self.accept('KW_AND'):
                self.result = ExprBinary('logical_and', 'AND', self.result, self.parse_expr_cmp())
            else:
                break

        return self.result


    def parse_expr_cmp(self):
        self.result = self.parse_expr_rel()

        while True:
            if self.accept('OP_IS_EQ'):
                self.result = ExprBinary('cmp', 'EQUAL', self.result, self.parse_expr_rel())
            elif self.accept('OP_IS_NEQ'):
                self.result = ExprBinary('cmp', 'NOT_EQUAL', self.result, self.parse_expr_rel())
            else:
                break

        return self.result


    def parse_expr_rel(self):
        self.result = self.parse_expr_sum_sub()

        while True:

            if self.accept('OP_G'):
                self.result = ExprBinary('rel', 'GREATER', self.result, self.parse_expr_sum_sub())
            elif self.accept('OP_GE'):
                self.result = ExprBinary('rel', 'GREATER_OR_EQUAL', self.result, self.parse_expr_sum_sub())
            elif self.accept('OP_L'):
                self.result = ExprBinary('rel', 'LESS', self.result, self.parse_expr_sum_sub())
            elif self.accept('OP_LE'):
                self.result = ExprBinary('rel', 'LESS_OR_EQUAL', self.result, self.parse_expr_sum_sub())
            else:
                break

        return self.result


    # <ADD> ::= <MULT> | <ADD> "+" <MULT>
    # <ADD> ::= <MULT> {("+" | "-") <MULT>}

    # older: <ADD> ::= <MULT> {OP_PLUS <MULT>}
    def parse_expr_sum_sub(self):
        self.result = self.parse_expr_mul_div_mod()

        while True:
            if self.accept('OP_SUM'):
                self.result = ExprBinary('arith', 'ADD', self.result, self.parse_expr_mul_div_mod())
            elif self.accept('OP_SUB'):
                self.result = ExprBinary('arith', 'SUB', self.result, self.parse_expr_mul_div_mod())
            else:
                break

        return self.result


    # <MULT> ::= <PRIMARY> | <MULT> "*" <PRIMARY>
    # <MULT> ::= <PRIMARY> {"*" <PRIMARY>}

    # older: <MULT> ::= <TERM> {OP_MULT <TERM>}
    def parse_expr_mul_div_mod(self):
        self.result = self.parse_expr_unary()

        # fixme useless while loop
        while True:
            if self.accept('OP_MUL'):
                self.result = ExprBinary('arith', 'MUL', self.result, self.parse_expr_unary())
            elif self.accept('OP_DIV'):
                self.result = ExprBinary('arith', self.result, self.parse_expr_unary())
            elif self.accept('OP_MOD'):
                self.result = ExprBinary('arith', self.result, self.parse_expr_unary())
            else:
                break

        return self.result

    def parse_expr_unary(self):
        if self.peek('OP_INCR') or self.peek('OP_DECR') or self.peek('OP_NOT'):
            return self.parse_expr_unary_prefix()
        else:
            return self.parse_expr_primary()


    def parse_expr_unary_prefix(self):
        if self.accept('OP_INCR'):
            op = 'INCREMENT'
        elif self.accept('OP_DECR'):
            op = 'DECREMENT'
        elif self.accept('OP_NOT'):
            op = 'NOT'
            op_count = 1
            while self.accept('OP_NOT'):
                op_count += 1
            name = self.expect('IDENT')
            return ExprUnaryPrefix(name, op, op_count)

        name = self.expect('IDENT')
        return ExprUnaryPrefix(name, op)

    # <PRIMARY> ::= <LIT_INT> | <VAR> | <PAREN>
    def parse_expr_primary(self):
        if self.peek('IDENT'):
            if self.peek2('OP_PAREN_O'):
                return self.parse_fn_call()
            else:
                return self.parse_expr_var()

        elif self.token_type() == 'LIT_INT':
            return self.parse_expr_lit_int()
        elif self.token_type() == 'LIT_FLOAT':
            return self.parse_expr_lit_float()
        elif self.token_type() == 'LIT_CHAR':
            return self.parse_expr_lit_char()
        elif self.token_type() == 'LIT_STR':
            return self.parse_expr_lit_str()
        if self.token_type() == 'KW_NULL':
            return self.parse_expr_lit_null()
        elif self.token_type() == 'KW_TRUE':
            return self.parse_expr_lit_true()
        elif self.token_type() == 'KW_FALSE':
            return self.parse_expr_lit_false()
        elif self.token_type() == 'OP_PAREN_O':
            return self.parse_expr_paren()
        else:
            self.error(f'expr error {self.curr_token}')


    def parse_expr_lit_int(self):
        lit = self.expect('LIT_INT')
        return ExprLit(lit, 'INT')

    def parse_expr_lit_float(self):
        lit = self.expect('LIT_FLOAT')
        return ExprLit(lit, 'FLOAT')

    def parse_expr_lit_char(self):
        lit = self.expect('LIT_CHAR')
        return ExprLit(lit, 'CHAR')

    def parse_expr_lit_str(self):
        lit = self.expect('LIT_STR')
        return ExprLit(lit, 'STR')

    def parse_expr_lit_null(self):
        lit = self.expect('KW_NULL')
        return ExprLit(lit, 'NULL')

    def parse_expr_lit_true(self):
        lit = self.expect('KW_TRUE')
        return ExprLit(lit, 'True')

    def parse_expr_lit_false(self):
        lit = self.expect('KW_FALSE')
        return ExprLit(lit, 'False')



    def parse_expr_paren(self):
        self.expect('OP_PAREN_O')
        self.result = self.parse_expr()
        self.expect('OP_PAREN_C')
        return self.result

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
        if self.peek('IDENT'):
            if self.peek2('OP_PAREN_O'):
                return self.parse_stmt_expr(self.parse_expr_fn_call())
            # todo refactor this mess
            for assign_op in ['OP_ASSIGN_EQ', 'OP_ASSIGN_SUM', 'OP_ASSIGN_SUB',
                          'OP_ASSIGN_MUL', 'OP_ASSIGN_DIV', 'OP_ASSIGN_MOD']:
                # todo refactor peek2 fn
                if self.peek2(assign_op):
                    return self.parse_stmt_assign()

        # fixme here it is specified what prefix operators are legit to be contained in a legit statement!
        # fixme vagueness
        elif self.token_type() in ['OP_INCR', 'OP_DECR']:
            return self.parse_stmt_expr(self.parse_expr_unary_prefix())

        if self.token_type() == 'KW_IF':
            return self.parse_stmt_if()
        if self.token_type() == 'KW_FOR':
            return self.parse_stmt_for()
        if self.token_type() == 'KW_WHILE':
            return self.parse_stmt_while()
        if self.token_type() == 'KW_BREAK':
            return self.parse_stmt_break()
        if self.token_type() == 'KW_CONTINUE':
            return self.parse_stmt_continue()
        if self.token_type() == 'KW_RETURN':
            return self.parse_stmt_ret()
        if self.token_type() in ['KW_BOOL', 'KW_FLOAT', 'KW_INT', 'KW_VOID', 'KW_CHAR', 'KW_STR']:
            return self.parse_stmt_var_decl()
        else:
            self.error(inspect.stack()[0][3])


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
        if_cond = self.parse_expr()
        self.expect('OP_PAREN_C')
        if_body = self.parse_stmt_block()

        elif_conds = []
        elif_bodies = []
        else_body = None

        if self.token_type() == 'KW_ELIF':

            while self.accept('KW_ELIF'):
                self.expect('OP_PAREN_O')
                elif_conds.append(self.parse_expr())
                self.expect('OP_PAREN_C')
                elif_bodies.append(self.parse_stmt_block())

        if self.token_type() == 'KW_ELSE':
            self.expect('KW_ELSE')
            else_body = self.parse_stmt_block()

        return StmtIf(if_cond, if_body, elif_conds, elif_bodies, else_body)


    # def parse_stmt_for(self):
    #     self.expect('KW_FOR')
    #     self.expect('OP_PAREN_O')
    #     for_init = self.parse_for_init()
    #     self.expect('OP_SEMICOLON')
    #     for_cond = self.parse_for_cond()
    #     self.expect('OP_SEMICOLON')
    #     for_incr = self.parse_for_incr()
    #     self.expect('OP_PAREN_C')
    #
    #     for_body = self.parse_stmt_block()
    #
    #     return StmtFor(for_init, for_cond, for_incr, for_body)

    def parse_for_cond(self):
        if self.peek('IDENT'):
            for assign_op in ['OP_ASSIGN_EQ', 'OP_ASSIGN_SUM', 'OP_ASSIGN_SUB',
                              'OP_ASSIGN_MUL', 'OP_ASSIGN_DIV', 'OP_ASSIGN_MOD']:
                if self.peek2(assign_op):
                    return self.parse_stmt_assign()
        else:
            self.result =  self.parse_expr()
            self.expect('OP_SEMICOLON')
            return self.result

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

    def parse_stmt_continue(self):
        continue_kw = self.expect('KW_CONTINUE')
        self.expect('OP_SEMICOLON')
        return StmtContinue(continue_kw)

    def parse_stmt_ret(self):
        return_kw = self.expect('KW_RETURN')

        if self.token_type() != 'OP_SEMICOLON':
            value = self.parse_expr()
        else:
            value = None

        self.expect('OP_SEMICOLON')

        return StmtReturn(return_kw, value)

    def parse_stmt_var_decl(self):
        type_ = self.parse_type()
        name = self.expect('IDENT')
        self.expect('OP_SEMICOLON')
        return StmtVarDecl(name, type_)

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
        elif self.token_type() == 'KW_CHAR':
            self.expect('KW_CHAR')
            return TypePrim('CHAR')
        elif self.token_type() == 'KW_STR':
            self.expect('KW_STR')
            return TypePrim('STR')
        else:
            self.error(inspect.stack()[0][3])

    def peek(self, token_type):
        self.curr_token = self.tokens[self.offset]
        if self.curr_token.type == token_type:
            return self.curr_token

    def peek2(self, next_token_type):
        next_token = self.tokens[self.offset + 1]
        return next_token.type == next_token_type

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


class ExprUnaryPrefix(Expr):

    def __init__(self, var, op, op_count=None):
        self.var = var
        self.op = op
        self.op_count = op_count
        super().__init__()

    def print_node(self, p):
        p.print('var', self.var)
        p.print_single('op', self.op)
        if self.op_count:
            p.print_single('op count', self.op_count)


class ExprBinary(Expr):

    # todo atribute list everywhere (with type hints)

    def __init__(self, kind, op, left, right):
        self.kind = kind
        self.op = op
        self.left = left
        self.right = right
        super().__init__()

    def print_node(self, p):
        p.print_single('kind', self.kind)
        p.print_single('op', self.op)
        p.print('left', self.left)
        p.print('right', self.right)

class ExprFnCall(Expr):

    def __init__(self, name, args):
        self.name = name
        self.args = args
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('args', self.args)


class ExprLit(Expr):

    def __init__(self, lit, kind):
        self.lit = lit
        self.kind = kind
        super().__init__()

    def print_node(self, p):
        p.print('lit', self.lit)
        p.print_single('kind', self.kind)


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

    def __init__(self, if_cond, if_body, elif_conds = None, elif_bodies = None, else_body = None):
        self.if_cond = if_cond
        self.if_body = if_body
        self.elif_conds = elif_conds
        self.elif_bodies = elif_bodies
        self.else_body = else_body
        super().__init__()

    def print_node(self, p):
        p.print('if_cond', self.if_cond)
        p.print('if_body', self.if_body)
        if self.elif_conds:
            for ind in range(len(self.elif_conds)):
                p.print(f'elif_cond[{ind}]', self.elif_conds[ind])
                p.print(f'elif_body[{ind}]', self.elif_bodies[ind])
        if self.else_body:
            p.print('else_body', self.else_body)

class StmtWhile(Stmt):

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)

class StmtExpr(Stmt):
    def __init__(self, expr):
        self.expr = expr
        super().__init__()

    def print_node(self, p):
        p.print('expr', self.expr)


class StmtBreak(Stmt):

    def __init__(self, break_kw):
        self.break_kw = break_kw
        super().__init__()

    def print_node(self, p):
        p.print('break_kw', self.break_kw)

class StmtContinue(Stmt):

    def __init__(self, continue_kw):
        self.continue_kw = continue_kw
        super().__init__()

    def print_node(self, p):
        p.print('continue_kw', self.continue_kw)


class StmtReturn(Stmt):

    def __init__(self, return_kw, value):
        self.return_kw = return_kw
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('return_kw', self.return_kw)
        p.print('value', self.value)

class StmtAssign(Stmt):

    def __init__(self, var, op, value):
        self.var = var
        self.op = op
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('var', self.var)
        p.print_single('op', self.op)
        p.print('value', self.value)

class StmtUnaryPrefix(Stmt):

    def __init__(self, expr_unary):
        self.expr_unary = expr_unary
        super().__init__()

    def print_node(self, p):
        # todo naming
        p.print('expr_unary_prefix', self.expr_unary)




class StmtVarDecl(Stmt):

    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)


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

