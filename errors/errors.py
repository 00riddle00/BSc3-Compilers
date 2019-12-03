from abc import abstractmethod
from pprint import pprint

user_friendly_names = {
    'KW_INCLUDE': '@',
    'KW_FN': 'fx',
    'KW_FN_RET_ARROW': '==',
    'KW_FN_IN': 'in',
    'KW_FN_OUT': 'out',
    'KW_IF': 'if',
    'KW_ELIF': 'elif',
    'KW_ELSE': 'else',
    'KW_FOR': 'for',
    'KW_WHILE': 'while',
    'KW_BREAK': 'break',
    'KW_CONTINUE': 'continue',
    'KW_RETURN': 'return',
    'KW_VOID': 'void',
    'KW_INT': 'int',
    'KW_FLOAT': 'float',
    'KW_BOOL': 'bool',
    'KW_CHAR': 'char',
    'KW_STR': 'string',
    'KW_STRUCT': 'struct',
    'KW_NULL': 'NULL',
    'KW_TRUE': 'True',
    'KW_FALSE': 'False',
    'KW_AND': 'AND',
    'KW_OR': 'OR',
    'IDENT': 'identifier',
    'LIT_INT': 'int literal',
    'LIT_FLOAT': 'float literal',
    'LIT_CHAR': 'char literal',
    'LIT_STR': 'string literal',
    'OP_G': '',
    'OP_GE': '=',
    'OP_L': '',
    'OP_LE': '=',
    'OP_IS_EQ': '==',
    'OP_IS_NEQ': '!=',
    'OP_SUM': '+',
    'OP_SUB': '-',
    'OP_MUL': '*',
    'OP_DIV': '/',
    'OP_MOD': '%',
    'OP_NOT': '!',
    'OP_INCR': '++',
    'OP_DECR': '--',
    'OP_ASSIGN_EQ': '=',
    'OP_ASSIGN_SUM': '+=',
    'OP_ASSIGN_SUB': '-=',
    'OP_ASSIGN_MUL': '*=',
    'OP_ASSIGN_DIV': '/=',
    'OP_ASSIGN_MOD': '%=',
    'OP_PTR': '$',
    'OP_PTR_ADDR': '&',
    'OP_DOT_ACCESS_MEMBER': '.',
    'OP_PTR_ACCESS_MEMBER': '-',
    'OP_PAREN_O': '(',
    'OP_PAREN_C': ')',
    'OP_BRACE_O': '{',
    'OP_BRACE_C': '}',
    'OP_BRACKET_O': '[',
    'OP_BRACKET_C': ']',
    'OP_SEMICOLON': ';',
    'OP_COMMA': ',',
}


class CompilerError(BaseException):

    def __init__(self, msg, file=None, line=None, pos=None):
        self.msg = msg
        self.file = file
        self.line = line
        self.pos = pos

    @abstractmethod
    def print_err(self):
        pass


class SemanticError(CompilerError):

    def print_err(self):
        print(f'SemanticERROR: {self.file}:{self.line}:{self.pos} {self.msg}')


class InputError(CompilerError):

    def print_err(self):
        print(f'[InputERROR] [{self.msg}]')


class LexerError(CompilerError):

    def print_err(self):
        print(f'LexerERROR: {self.file}:{self.line}:{self.pos} {self.msg}')


class LexerDebugError(LexerError):
    def __init__(self, msg, file=None, line=None, pos=None, state=None, curr_char=None, buffer=None):
        super().__init__(msg, file, line, pos)
        self.state = state
        self.curr_char = curr_char
        self.buffer = buffer

    def print_err(self):
        top_right_delim = 33 * '!'
        top_left_delim = 33 * '!'
        v_delim = 5 * '!'
        bottom_delim = 81 * '!'

        print(f'{top_left_delim} [Lexer error] {top_right_delim}')
        print(f'{v_delim} [file={self.file}: line={self.line}: position={self.pos}]')
        print(f'{v_delim} [Error message]: {self.msg}'),
        if self.buffer:
            print(f'{v_delim} [Item being lexed (pretty print)]:'),
            pprint(self.buffer + self.curr_char)
        print(f'{v_delim} [state]: {self.state}')
        print(f'{v_delim} [output so far]:')
        print(bottom_delim)


class ParserError(CompilerError):

    def __init__(self, msg, file=None, line=None, pos=None, exp_token=None, curr_token=None):
        super().__init__(msg, file, line, pos)
        self.exp_token = exp_token
        self.curr_token = curr_token

    def print_err(self):
        exp = self.exp_token
        if exp in user_friendly_names.keys():
            exp = user_friendly_names[exp]
        print(f'ParserERROR: {self.file}:{self.line}:{self.pos} '
              f'expected({exp}), found({user_friendly_names[self.curr_token]})')


class ParserDebugError(ParserError):
    pass
