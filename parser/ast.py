class Node(object):

    def __init__(self):
        pass

    def print_node(self, p):
        print(f'print not implemented for {self.__class__}')


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


class Expr(Node):

    def __init__(self):
        pass
        super().__init__()


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


class ExprUnaryPrefix(Expr):

    def __init__(self, var, op, op_count=1):
        self.var = var
        self.op = op
        self.op_count = op_count
        super().__init__()

    def print_node(self, p):
        p.print('var', self.var)
        p.print_single('op', self.op)
        if self.op_count > 1:
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


class Decl(Node):

    def __init__(self):
        pass
        super().__init__()


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


class IfBranch(Node):

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)


class IfCondition(Expr):

    def __init__(self, expr):
        self.expr = expr
        super().__init__()

    def print_node(self, p):
        p.print('expr', self.expr)


class IfBody(StmtBlock):

    def __init__(self, stmts):
        super().__init__(stmts)

    def print_node(self, p):
        super().print_node(p)


class StmtIf(Stmt):

    def __init__(self, branches, stmt_block=None):
        self.branches = branches
        self.stmt_block = stmt_block
        super().__init__()

    def print_node(self, p):
        for ind in range(len(self.branches)):
            p.print(f'branch[{ind}]', self.branches[ind])
        if self.stmt_block:
            p.print(f'else', self.stmt_block)


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


class StmtExpr(Stmt):
    def __init__(self, expr):
        self.expr = expr
        super().__init__()

    def print_node(self, p):
        p.print('expr', self.expr)


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


class StmtVarDecl(Stmt):

    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)
