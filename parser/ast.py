class Node(object):

    def __init__(self):
        pass

    def print_node(self, p):
        print(f'print not implemented for {self.__class__}')


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


class Param(Node):

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


class StmtBlock(Node):

    def __init__(self, stmts):
        self.stmts = stmts
        super().__init__()

    def print_node(self, p):
        p.print('stmts', self.stmts)


class Stmt(Node):

    def __init__(self):
        pass
        super().__init__()


class IfBranch(Node):

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)


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
        p.print('keyword', self.break_kw)


class StmtContinue(Stmt):

    def __init__(self, continue_kw):
        self.continue_kw = continue_kw
        super().__init__()

    def print_node(self, p):
        p.print('keyword', self.continue_kw)


class StmtReturn(Stmt):

    def __init__(self, return_kw, value=None):
        self.return_kw = return_kw
        self.value = value
        super().__init__()

    def print_node(self, p):
        if not self.value:
            p.print('keyword', self.return_kw)
        else:
            p.print('value', self.value)


class StmtVarDecl(Stmt):

    def __init__(self, name, type_):
        self.name = name
        self.type = type_
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)


class StmtAssign(Stmt):

    def __init__(self, lhs, op, value):
        self.lhs = lhs
        self.op = op
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('lhs', self.lhs)
        p.print_single('op', self.op)
        p.print('value', self.value)


class StmtExpr(Stmt):
    def __init__(self, expr):
        self.expr = expr
        super().__init__()

    def print_node(self, p):
        p.print('expr', self.expr)


class Expr(Node):

    def __init__(self):
        pass
        super().__init__()


class ExprFnCall(Expr):

    def __init__(self, name, args):
        self.name = name
        self.args = args
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('args', self.args)


class ExprBinary(Expr):

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


class ExprUnary(Expr):

    def __init__(self, inner, op):
        self.inner = inner
        self.op = op
        super().__init__()

    def print_node(self, p):
        p.print('inner', self.inner)
        p.print_single('op', self.op)


class ExprVar(Expr):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)


class ExprLit(Expr):

    def __init__(self, lit, kind):
        self.lit = lit
        self.kind = kind
        super().__init__()

    def print_node(self, p):
        p.print('lit', self.lit)
        p.print_single('kind', self.kind)
