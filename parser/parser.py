from pprint import pprint
from lexer import Token, Input
from errors import ParserError
import inspect
from .ast import Node, TypePrim, ExprLit, ExprVar, ExprUnaryPrefix, ExprBinary, \
    ExprFnCall, Param, Program, DeclFn, StmtBlock, StmtIf, StmtWhile, StmtBreak, \
    StmtContinue, StmtReturn, StmtExpr, StmtAssign, StmtVarDecl, \
    IfBody, IfBranch, IfCondition

assign_ops = {
    'OP_ASSIGN_EQ': 'EQUALS',
    'OP_ASSIGN_SUM': 'PLUS_EQUALS',
    'OP_ASSIGN_SUB': 'MINUS_EQUALS',
    'OP_ASSIGN_MUL': 'MULT_EQUALS',
    'OP_ASSIGN_DIV': 'DIV_EQUALS',
    'OP_ASSIGN_MOD': 'MOD_EQUALS',
}


class Parser:
    curr_input: Input
    tokens: list
    offset: int
    curr_token: Token
    result: Node

    def __init__(self, curr_input, tokens) -> None:
        self.curr_input = curr_input
        self.tokens = tokens
        self.offset = 0
        self.result = Node()

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
            raise ParserError(self, '', token_type)

    def parse_stmt_assign(self):
        # todo do not allow var to be keyword (ex TRUE, NULL)
        var = self.expect('IDENT')

        op = ''

        if self.token_type() in assign_ops.keys():
            self.expect(self.token_type())
            op = assign_ops[self.token_type()]
        else:
            raise ParserError(self, 'invalid assign op')

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

    def parse_expr_mul_div_mod(self):
        self.result = self.parse_expr_unary()

        # fixme useless while loop
        while True:
            if self.accept('OP_MUL'):
                self.result = ExprBinary('arith', 'MUL', self.result, self.parse_expr_unary())
            elif self.accept('OP_DIV'):
                self.result = ExprBinary('arith', 'DIV', self.result, self.parse_expr_unary())
            elif self.accept('OP_MOD'):
                self.result = ExprBinary('arith', 'MOD', self.result, self.parse_expr_unary())
            else:
                break

        return self.result

    def parse_expr_unary(self):
        if self.peek('OP_INCR') or self.peek('OP_DECR') or self.peek('OP_NOT'):
            return self.parse_expr_unary_prefix()
        else:
            return self.parse_expr_primary()

    def parse_expr_unary_prefix(self):
        op = ''

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

    def parse_expr_primary(self):
        if self.peek('IDENT'):
            if self.peek2('OP_PAREN_O'):
                return self.parse_expr_fn_call()
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
            raise ParserError(self, f'expr error {self.curr_token}')

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
            for assign_op in assign_ops.keys():
                # todo refactor peek2 fn
                if self.peek2(assign_op):
                    return self.parse_stmt_assign()

        # fixme here it is specified what prefix operators are legit to be contained in a legit statement!
        # fixme vagueness
        elif self.token_type() in ['OP_INCR', 'OP_DECR']:
            return self.parse_stmt_expr(self.parse_expr_unary_prefix())

        if self.token_type() == 'KW_IF':
            return self.parse_stmt_if()
        # if self.token_type() == 'KW_FOR':
        #     return self.parse_stmt_for()
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
            raise ParserError(self, f'called from fn: {inspect.stack()[0][3]}')

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
        if_cond = IfCondition(self.parse_expr())
        self.expect('OP_PAREN_C')
        if_body = IfBody(self.parse_stmt_block())

        if_branch = IfBranch('if', if_cond, if_body)

        elif_branches = None
        else_branch = None

        if self.token_type() == 'KW_ELIF':
            elif_branches = []

            while self.accept('KW_ELIF'):
                self.expect('OP_PAREN_O')
                elif_cond = IfCondition(self.parse_expr())
                self.expect('OP_PAREN_C')
                elif_body = IfBody(self.parse_stmt_block())
                elif_branches.append(IfBranch('elif', elif_cond, elif_body))

        if self.token_type() == 'KW_ELSE':
            self.expect('KW_ELSE')
            else_cond = None
            else_body = IfBody(self.parse_stmt_block())
            else_branch = IfBranch('else', else_cond, else_body)

        return StmtIf(if_branch, elif_branches, else_branch)

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
            for assign_op in assign_ops.keys():
                if self.peek2(assign_op):
                    return self.parse_stmt_assign()
        else:
            self.result = self.parse_expr()
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
            raise ParserError(self, f'called from fn: {inspect.stack()[0][3]}')

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
