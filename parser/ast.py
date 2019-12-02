from lexer import Token


# make global variable
# curr_stack_slot = 0


def raise_error(msg):
    print(msg)
    exit(1)


def std_error(msg):
    print(msg)
    exit(1)


def semantic_error(message, token=None):
    line_no = token.line_no if (token and token.line_no) else '?'
    std_error(f'???:{line_no}: semantic error: {message}')
    exit(1)


# ar dvi sakos sutampa
# gali ateiti nil nes vykdome vardu rezoliucija,
# ne tik tipu tikrinima. ji gali feilinti. analize darom kai TIK pavyksta...


def unify_types(type_0, type_1):
    err = unify(type_0, type_1)
    if err == 0:
        return True
    elif err == 1:
        semantic_error(f'type mismatch: expected {type_0.unwrap()}, got {type_1.unwrap()}')
    elif err == 2:
        # ar token visgi paduoti i sem err?
        semantic_error(f'type kind mismatch: expected {type_0.kind}, got {type_1.kind}')


# Node.check_type_eq() <- gal i vidu ikelti?
def unify(type_0, type_1):
    # def unify_types(type_0, type_1, token=None):
    # todo error?
    if not type_0 or not type_1:
        return 0
    elif type_0.__class__ != type_1.__class__:
        return 1
    # cia jau zinome kad klases sutampa (TypePrim?)
    elif isinstance(type_0, TypePointer) and isinstance(type_1, TypePointer):
        return unify(type_0.inner, type_1.inner)
    elif isinstance(type_0, TypePrim) and isinstance(type_1, TypePrim):
        if type_0.kind != type_1.kind:
            return 2
        else:
            return 0
    else:
        raise_error('unreachable')


class Scope:

    def __init__(self, parent_scope=None):
        self.members = {}
        self.parent_scope = parent_scope

    def add(self, name, node):
        if not isinstance(name, Token) or not isinstance(node, Node):
            raise TypeError

        # if node.respond_to?(:stack_slot):
        # node.stack_slot = $curr_stack_slot
        # $curr_stack_slot += 1
        # end

        # todo maybe name.value is not among keys() at all (?)
        if name.value not in self.members.keys() or not self.members[name.value]:
            self.members[name.value] = node
        else:
            # todo ensure print line
            semantic_error(f'duplicate variable: {name.value}', name)

    def resolve(self, name):
        if not isinstance(name, Token):
            raise TypeError

        if name.value in self.members.keys():
            # todo check for None/False
            node = self.members[name.value]
            return node
        elif self.parent_scope:
            # todo return?
            return self.parent_scope.resolve(name)
        else:
            semantic_error(f'undeclared variable: {name.value}', name)
            # return nil


# abstract
# virtual Type* check_types() = 0;
class Node(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.target_node = None
        pass

    def unwrap(self):
        return self.__class__.__name__

    # def allocate_slots
    # end

    # def check_types
    #     raise 'not implemented %s' % [self.class]
    # end

    # def compile(pw)
    #     raise 'not implemented %s' % [self.class]
    # end
    #
    # def is_const?
    #     true
    # end

    # def output(indent, str)
    #     puts("#{'  ' * indent}#{str}")
    # end

    # def print(indent=0)
    #     output(indent, "?????")
    # end
    def resolve_names(self, scope):
        # raise NotImplementedError.new
        raise_error(f'resolve names not implemented for: {self.__class__.__name__}')

    def add_children(self, *children):
        for child in children:
            if not child:
                pass  # ignore
            elif type(child) == list:
                for ch in child:
                    self.add_children(ch)
            elif isinstance(child, Node):
                child.parent = self
            else:
                raise_error('bad child')

    # or ancestor_class = node_class
    # or ancestor_fn
    def find_ancestor(self, ancestor_class):
        current_node = self.parent
        while current_node:
            # or ancestor_class = DefFn
            if isinstance(current_node, ancestor_class):
                return current_node
            else:
                current_node = current_node.parent

    def ancestor_loop(self):
        current = self.parent
        while current:
            if isinstance(current, StmtWhile):
                return current
            else:
                current = current.parent

    def print_node(self, p):
        print(f'print not implemented for {self.__class__}')

    def check_types(self):
        # raise NotImplementedError
        raise_error(f'check_types not implemented for {self.__class__}')


class Program(Node):
    # attr_reader :decls
    # or attr_accessor :decls

    # std::vector<Decl*>
    def __init__(self, decls):
        self.add_children(*decls)
        self.decls = decls
        super().__init__()

    def print_node(self, p):
        p.print('decls', self.decls)

    def resolve_names(self, scope):
        for decl in self.decls:
            scope.add(decl.name, decl)
        for decl in self.decls:
            decl.resolve_names(scope)

    # todo return value?
    def check_types(self):
        for decl in self.decls:
            decl.check_types()


# abstract
class Decl(Node):

    def __init__(self):
        pass
        super().__init__()


class DeclFn(Decl):
    # attr_reader :name, :params, :ret_type, :body
    # attr_accessor :name
    # attr_accessor :params
    # attr_accessor :ret_type
    # attr_accessor :body
    # attr_reader :entry_label

    # attr_reader :builtin
    num_locals: int
    local_count: int

    # todo params -> *args?
    def __init__(self, name, params, ret_type, body):
        self.add_children(params + [ret_type] + [body])
        self.name = name
        self.params = params
        self.ret_type = ret_type
        self.body = body
        # todo whatis?
        # self.entry_label = Label.new
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('params', self.params)
        p.print('ret_type', self.ret_type)
        p.print('body', self.body)

    def resolve_names(self, scope):
        # scope.add(@name, self) 2017 buvo
        inner_scope = Scope(scope)
        # curr_stack_slot = 0  # todo or $slot_index
        for param in self.params:
            inner_scope.add(param.name, param)
        # self.num_locals = curr_stack_slot
        # self.local_count = curr_stack_slot - len(self.params)
        self.body.resolve_names(inner_scope)

    def check_types(self):
        for param in self.params:
            param.check_types()
        self.body.check_types()


class Param(Node):

    # attr_accessor :slot_index

    def __init__(self, name, type_):
        # todo is this add_children needed here?
        self.add_children(type_)
        self.name = name
        self.type = type_
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)

    #     def resolve_names(scope)
    #         scope.add(@name, self)
    #         end
    #     end

    def check_types(self):
        if not self.type.has_value():
            semantic_error(f'parameter\'s type cannot be void or pointer to void')


# abstract
class Type(Node):

    # def == (other)
    #     self.class == other.class
    # end

    def __init__(self):
        pass
        super().__init__()

    def is_arithmetic(self):
        return False

    def has_value(self):
        return False

    def is_comparable(self):
        return False


# class TypeBool < TypePrim # or tsg Type?
#     def print(p)
#         end
#
#     def to_s
#         'bool'
#     end
# end
#
# class TypeInt < TypePrim
#     def print(p)
#         end
#
#     def to_s
#         'int'
#     end
# end
#
# class TypeVoid < TypePrim
#     def print(p)
#         end
#
#     def to_s
#         'void'
#     end
# end
#


class TypePointer(Type):

    def __init__(self, inner):
        # todo is add_children needed here?
        self.add_children(inner)
        self.inner = inner
        super().__init__()

    def print_node(self, p):
        p.print('inner', self.inner)

    def has_value(self):
        return self.inner.has_value()

    def unwrap(self, depth=1):
        if isinstance(self.inner, TypePointer):
            return self.inner.unwrap(depth + 1)
        elif isinstance(self.inner, TypePrim):
            return f'{self.inner.kind}{depth * "$"}'
        else:
            raise_error('pointer to something other than primary type')

    # todo is it needed?
    # def resolve_names(self, scope):
    #     ...


class TypePrim(Type):

    def __init__(self, kind):
        self.kind = kind
        # todo is it needed? (token=None)
        # self.token = token
        super().__init__()

    def print_node(self, p):
        p.print_single('kind', self.kind)

    def is_arithmetic(self):
        return self.kind == 'FLOAT' or self.kind == 'INT'

    # jei tipas reiksme tures su kuria operacijas galim atlikti
    def has_value(self):
        return self.kind != 'VOID'

    def is_comparable(self):
        return self.kind == 'INT' or self.kind == 'BOOL'
        # return self.kind == 'FLOAT' or self.kind == 'INT' ??

    def unwrap(self):
        return self.kind


class StmtBlock(Node):

    def __init__(self, stmts):
        self.add_children(stmts)
        # self.add_children(*stmts)
        self.stmts = stmts
        super().__init__()

    # def empty?
    #     @statements.empty?
    # end

    def print_node(self, p):
        p.print('stmts', self.stmts)

    def resolve_names(self, scope):
        inner_scope = Scope(scope)  # or child scope
        for stmt in self.stmts:
            stmt.resolve_names(inner_scope)

    def check_types(self):
        for stmt in self.stmts:
            stmt.check_types()


# abstract
class Stmt(Node):

    def __init__(self):
        pass
        super().__init__()


class IfBranch(Node):

    def __init__(self, cond, body):
        self.add_children(cond, body)
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)

    def resolve_names(self, scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)


class StmtIf(Stmt):

    def __init__(self, branches, else_block=None):
        self.add_children(branches, else_block)
        self.branches = branches
        self.else_block = else_block
        super().__init__()

    def print_node(self, p):
        for ind in range(len(self.branches)):
            p.print(f'branch[{ind}]', self.branches[ind])
        if self.else_block:
            p.print(f'else', self.else_block)

    def resolve_names(self, scope):
        # fixme cond=branches, body=else_block
        for branch in self.branches:
            branch.resolve_names(scope)
        if self.else_block:
            self.else_block.resolve_names(scope)

    def check_types(self):
        # fixme cond=branches, body=else_block
        # cond_type = self.cond.check_types()
        # unify_types(cond_type, TYPE_BOOL)
        # todo return?
        # self.body.check_types()
        pass


class StmtFor(Stmt):

    def __init__(self, for_init, for_cond, for_step, for_body):
        self.add_children(for_init, for_cond, for_step, for_body)
        self.for_init = for_init
        self.for_cond = for_cond
        self.for_step = for_step
        self.for_body = for_body
        super().__init__()

    def print_node(self, p):
        p.print('init', self.for_init)
        p.print('cond', self.for_cond)
        p.print('step', self.for_step)
        p.print('body', self.for_body)

    def resolve_names(self, scope):
        self.for_init.resolve_names(scope)
        self.for_cond.resolve_names(scope)
        self.for_step.resolve_names(scope)
        self.for_body.resolve_names(scope)


# panasiai kaip su if
# tikr tipus salygoje
# ...
class StmtWhile(Stmt):

    def __init__(self, cond, body):
        self.add_children(cond, body)
        self.cond = cond
        self.body = body
        super().__init__()

    def print_node(self, p):
        p.print('cond', self.cond)
        p.print('body', self.body)

    def resolve_names(self, scope):
        self.cond.resolve_names(scope)
        self.body.resolve_names(scope)

    def check_types(self):
        cond_type = self.cond.check_types()
        unify_types(cond_type, TYPE_BOOL)
        self.body.check_types()


# fixme from old file
class StmtBreak(Stmt):

    def __init__(self, break_kw):
        self.break_kw = break_kw
        super().__init__()

    def print_node(self, p):
        p.print('keyword', self.break_kw)

    def resolve_names(self, scope):
        curr_node = self.parent
        while curr_node:
            if isinstance(curr_node, StmtWhile) or isinstance(curr_node, StmtFor):
                self.target_node = curr_node
                break
            else:
                curr_node = curr_node.parent

        if not self.target_node:
            std_error(f'break not inside a loop statement: {self.break_kw.line_no}')

    def check_types(self):
        # do nothing?
        # fixme is it correct?
        # or target_node ??
        self.target_loop = self.ancestor_loop()  # or ancestor_while
        # @target = find_ancestor(WhileStatement)
        if not self.target_loop:
            std_error('break not in loop')


class StmtContinue(Stmt):

    def __init__(self, continue_kw):
        self.continue_kw = continue_kw
        super().__init__()

    def print_node(self, p):
        p.print('keyword', self.continue_kw)


# koks gi pas mus ret type?
class StmtReturn(Stmt):
    # unique_ptr<Expr> value;

    def __init__(self, return_kw, value=None):
        self.add_children(value)
        self.return_kw = return_kw
        self.value = value
        super().__init__()

    def print_node(self, p):
        if not self.value:
            p.print('keyword', self.return_kw)
        else:
            p.print('value', self.value)

    def resolve_names(self, scope):
        if self.value:
            self.value.resolve_names(scope)

    # todo ret_type <- method?
    def check_types(self):
        # ret_type = ancestor_fn.ret_type
        # ret_type = find_ancestor(&DeclFn)
        ret_type = self.find_ancestor(DeclFn).ret_type()
        # todo pythonize?
        # &. iskvies fn jei n...
        value_type = self.value.check_types() if self.value and self.value.check_types() else TypePrim('VOID')
        unify_types(ret_type, value_type)
        # unify_types(ret_type, value_type, @return_kw)


# var a: int = 5
class StmtVarDecl(Stmt):
    # attr_accessor :slot_index

    def __init__(self, name, type_, value=None):
        # todo do I need to add type_ here?
        self.add_children(type_, value)
        self.name = name
        self.type = type_
        self.value = value
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('type', self.type)
        if self.value:
            p.print('value', self.value)

    def resolve_names(self, scope):
        scope.add(self.name, self)
        if self.value:
            self.value.resolve_names(scope)

    def check_types(self):
        if not self.type.has_value():
            semantic_error(f'variable\'s type cannot be void or pointer to void')
        if self.value:
            value_type = self.value.check_types()
            unify_types(self.type, value_type)


class StmtAssign(Stmt):

    def __init__(self, lhs, op, value):
        self.add_children(value)
        self.lhs = lhs
        self.op = op
        self.value = value
        super().__init__()

    def print_node(self, p):
        # or lhs = target
        p.print('lhs', self.lhs)
        p.print_single('op', self.op)
        p.print('value', self.value)
        # p.print('target_node', @target_node.class.to_s)

    def resolve_names(self, scope):
        # todo lhs=var
        # self.lhs ExprVar yra, o ne token. Turi eiti gylyn gylyn, kol token ras (ir pointeriai ten viduj, etc.
        # todo put this under suspicion
        self.target_node = self.lhs.resolve_names(scope)
        # self.target_node = scope.resolve(self.lhs)
        self.value.resolve_names(scope)

    def check_types(self):
        target_type = None

        # todo jei exprunary nebutinai targetnode type
        if self.target_node:
            target_type = self.lhs.check_types()
            # target_type = @target.type
        # print(target_type.inner.kind)
        value_type = self.value.check_types()  # jis visada kazkoks bus, nereik tikrint kasd jis su void bus

        # todo return?
        # target_node jau prisyreme vardu rez metu
        # unifyt_types(@target_node&.type, value_type)
        # cia jei target_type nera, tai nil paduoti, ir viduj jau error gausim
        if target_type:
            unify_types(target_type, value_type)
        else:
            raise_error("no target type")


# def to_s
#     '%s' % [@kind]
# end

class StmtExpr(Stmt):

    def __init__(self, expr):
        self.add_children(expr)
        self.expr = expr
        super().__init__()

    def print_node(self, p):
        p.print('expr', self.expr)

    def resolve_names(self, scope):
        self.expr.resolve_names(scope)

    def check_types(self):
        # ar self.name?
        return self.expr.check_types()


# class StmtLet
#     def resolve_names(scope)
#         scope.add(@name, self)
#         end
#     end

# abstract
class Expr(Node):

    def __init__(self):
        pass
        super().__init__()


# foo(a, b, c + 5)
class ExprFnCall(Expr):

    def __init__(self, name, args):
        self.add_children(args)
        self.add_children(*args)
        self.name = name
        self.args = args
        if self.name.value in ('in', 'disp'):
            self.builtin = True
        else:
            self.builtin = False
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)
        p.print('args', self.args)
        # p.print('builtin', self.builtin)

    def resolve_names(self, scope):
        if not self.builtin:
            self.target_node = scope.resolve(self.name)
        else:
            # self.target_node = ???
            pass  # todo

        for arg in self.args:
            arg.resolve_names(scope)

    def check_types(self):
        # masyvui args ev. velemntui pritaikau fn check_types ir nauja masyva turi
        arg_types = [arg.check_types() for arg in self.args]

        # ar daiktas i kuri kreipiames apskr. egzistuoj?
        if not self.target_node:
            return
        elif not isinstance(self.target_node, DeclFn):
            semantic_error('the call target is not a function', self.name)
            return

        # zinome, kad radome fja, i kuria kreipemes
        # todo is type() a fn?
        param_types = [param.type() for param in self.target_node.params]
        if len(param_types) != len(arg_types):
            semantic_error(f'invalid argument count; expected {len(param_types)}, got {len(arg_types)}', self.name)

        # min tarp dvieju skaiciu koks?
        param_count = min(len(param_types), len(arg_types))
        for i in range(0, param_count):
            param_type = param_types[i]  # arba self.target.params[i].type()
            arg_type = arg_types[i]  # arba args[i].check_type()
            # patikrinu bent kazkiek tai argsu kiek ju yra.
            # pvz fjoj prasyta bent 4 param, o pateikiu bent 2 args, tai patikrinu bent tuos du
            # jei fjojs 1 arg parasyta, o pateikiu 2, tai patikrinu tik ta viena.
            unify_types(param_type, arg_type)

        # kazka pasakau koks cia tipas etc...
        return self.target_node.ret_type()


class ExprBinary(Expr):

    def __init__(self, kind, op, left, right):
        self.add_children(left, right)
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

    def resolve_names(self, scope):
        self.left.resolve_names(scope)
        self.right.resolve_names(scope)


# visiem binary op negalim parasyti viena tipu tikr klases
# class ExprBinary

# ExprArith: T + T -> T
# ExprLogic: B | B -> B
# ExprEquality: T == T -> B
# ExprComparison: T < T -> B

# Arithmetic expressions: a + b, a * b
# Comparison expressions: a > b, a < b => BOOL
# Boolean expressions: a && b, a || b

# Arithmatic Exprs: + - / * %
# Relational Exprs: < > >= <=
# Equality Exprs: != ==
# Boolean Exprs: && ||

# type+type -> type; is_arithmetic (bool+bool wrong, etc.)

# ExprBinArith: TYPE + TYPE -> TYPE; is_arithmetic
# class ExprBinArith < ExprBinary
# end
# virsta abs klase. Parseryje irgi pakeisti sita, kad grazinti konkrecias klases, o ne ExprBinary
class ExprBinArith(ExprBinary):

    # veliau turesim kiek praplesti sita aritm israisk
    def check_types(self):
        left_type = self.left.check_types()
        right_type = self.right.check_types()

        # turet omeny kad ir voidas i kaire puse gali ateit!
        if left_type and left_type.is_arithmetic:
            unify_types(left_type, right_type)
        else:
            # nezinom kurioj vietoj
            semantic_error(f'cannot perform arithmetic operations with this type: {left_type}')

        return left_type  # nres reik grazinti tipa taip mums


# ExprBinComparison: TYPE < TYPE -> BOOL; is_comparable
# class ExprBinComparison < ExprBinary
# end
# type < type -> bool; is_comparable (bool siaip jau nelabai compariname)
# monoton didjancios
# exprbinquality: type == type -> bool; has_value (tik = arba != (neturi buti voidas))
class ExprBinComparison(ExprBinary):  # > < == !=

    def check_types(self):
        left_type = self.left.check_types()
        right_type = self.right.check_types()

        # nes desine puse netikrint, nes jei ten bus null ar pan,
        # tai priklausys nuo LHS desine puse ir failins unify_types
        if left_type and left_type.is_comparable():
            unify_types(left_type, right_type)
        else:
            # nezinom kurioj vietoj
            semantic_error(f'cannot compare values of this type: {left_type}')

        # unify_types(left_type, right_type)
        # TypeBool.new
        # TYPE_BOOL
        return TypePrim('BOOL')


# ExprBinEquality: TYPE == TYPE -> BOOL; has_value
# class ExprBinEquality < ExprBinary
# end
class ExprBinEquality(ExprBinary):

    def check_types(self):
        left_type = self.left.check_types()
        right_type = self.right.check_types()
        if left_type and left_type.has_value():
            unify_types(left_type, right_type)
        else:
            semantic_error(f'this type has no value to compare: {left_type}')
        return TypePrim('BOOL')


# ExprBinLogic: BOOL || BOOL -> BOOL
# class ExprBinLogic < ExprBinary
# end
# visada left=bool, right=bool
class ExprBinLogic(ExprBinary):

    def check_types(self):
        left_type = self.left.check_types()
        right_type = self.right.check_types()
        unify_types(TYPE_BOOL, left_type)
        # TODO reverse order everywhere as well (left-param - expected type, right-param - got)
        unify_types(TYPE_BOOL, right_type)
        return TYPE_BOOL


# class ExprPrio < Expr
#     def initialize(inner)
#         @inner = inner
#     end
#
#     def print(p)
#         p.print 'inner', @inner
#     end

# def resolve_names(self, scope):
#     self.inner.resolve_names(scope)
# end
# end

class ExprUnary(Expr):

    def __init__(self, inner, op):
        self.add_children(inner)
        self.inner = inner
        self.op = op
        super().__init__()

    def print_node(self, p):
        p.print('inner', self.inner)
        p.print_single('op', self.op)

    def resolve_names(self, scope):
        self.target_node = self.inner.resolve_names(scope)
        return self.target_node

    def check_types(self):
        if self.op == 'PTR_ADDR':
            # todo is it pointer, pointer value literal or just int?
            if isinstance(self.inner, ExprUnary):
                semantic_error('wrong value to address')
            return TypePointer(self.target_node.type)
        # todo recursion
        elif self.op == 'PTR_DEREF':
            target_inner = self.target_node.type.inner
            inner = self.inner
            # todo del PTR_ADDR galimybes??
            while isinstance(inner, ExprUnary):
                if not inner.op == "PTR_DEREF":
                    semantic_error('value to dereference is not a pointer')
                if isinstance(target_inner, TypePointer):
                    inner = inner.inner
                    target_inner = target_inner.inner
                else:
                    semantic_error('primary type cannot be dereferenced')
            return target_inner
        elif self.target_node:
            return self.target_node.type


class ExprVar(Expr):

    def __init__(self, name):
        self.name = name
        # todo why is that?
        # self.target = None
        super().__init__()

    def print_node(self, p):
        p.print('name', self.name)

    def resolve_names(self, scope):
        self.target_node = scope.resolve(self.name)
        return self.target_node

    def check_types(self):
        # t-node jau vardu rez metu priskyreme jam (varui)
        # @target_node&.type #(jei kairej nil, arba abiejose sides nil, tai skipinam unify types (remember))
        if self.target_node:  # arba if @target.respond_to?(:type)
            return self.target_node.type


class ExprLit(Expr):

    def __init__(self, lit, kind):
        self.lit = lit
        self.kind = kind
        super().__init__()

    def print_node(self, p):
        p.print('lit', self.lit)
        p.print_single('kind', self.kind)

    def resolve_names(self, scope):
        pass  # do nothing

    def check_types(self):
        if self.lit.type == 'LIT_INT':
            return TYPE_INT
        elif self.lit.type == 'LIT_FLOAT':
            return TYPE_FLOAT
        elif self.lit.type in ['KW_TRUE', 'KW_FALSE']:
            return TYPE_BOOL
        elif self.lit.type == 'LIT_CHAR':
            return TYPE_CHAR
        elif self.lit.type == 'LIT_STR':
            return TYPE_STRING
        else:
            raise_error('Bad ExprLit token')


TYPE_VOID = TypePrim('VOID')
TYPE_INT = TypePrim('INT')
TYPE_FLOAT = TypePrim('FLOAT')
TYPE_BOOL = TypePrim('BOOL')
TYPE_CHAR = TypePrim('CHAR')
TYPE_STRING = TypePrim('STRING')
