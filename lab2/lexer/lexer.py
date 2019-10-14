from pprint import pprint

KEYWORDS = {
    'fx': ':KW_FN',
    'if': ':KW_IF',
    'elif': ':KW_ELIF',
    'else': ':KW_ELSE',
    'for': ':KW_FOR',
    'while': ':KW_WHILE',
    'break': ':KW_BREAK',
    'continue': ':KW_CONTINUE',
    'return': ':KW_RETURN',
    'int': ':KW_INT',
    'float': ':KW_FLOAT',
    'bool': ':KW_BOOL',
    'char': ':KW_CHAR',
    'string': ':KW_STRING',
    'struct': ':KW_STRUCT',
}


class Token:

    type_: str
    value: str
    line_no: int

    def __init__(self, type_, value, line_no):
        self.type = type_
        self.value = value
        self.line_no = line_no


class Lexer:
    buffer: str
    _input: str
    line_no: int
    offset: int
    state: str
    tokens: list
    token_start: int
    token_start_ln: int
    running: bool
    curr_char: str

    def __init__(self, _input) -> None:
        self.buffer = ''
        self._input = _input
        self.line_no = 1
        self.offset = 0
        self.state = ':START'
        self.tokens = []
        self.token_start = 0
        self.token_start_ln = 1
        self.running = True
        self.curr_char = ''

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.token_start_ln = self.line_no
        self.state = new_state

    def complete_ident(self):
        self.rewind()

        if self.buffer in KEYWORDS:
            kw_type = KEYWORDS[self.buffer]
            self.buffer = ''
            self.complete_token(kw_type)  # , False)
        else:
            self.complete_token(':IDENT')  # , False)

    def complete_token(self, token_type, advance=True, delta=0):
        self.tokens.append(Token(token_type, self.buffer, self.token_start_ln))
        # print(f'token: {token_type} {self.buffer}')
        self.buffer = ''
        self.state = ':START'
        self.offset += delta
        # arba viskas be advance
        if not advance:
            self.offset -= 1

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<10} | {"VALUE":<10}')
        for index, token in enumerate(self.tokens):
            print(f'{index:>3}| {token.line_no:>3}| {token.type:<10} | {token.value:<10}')

    def lex_all(self):
        while self.running and self.offset < len(self._input):
            self.curr_char = self._input[self.offset]
            # if self.curr_char == '\n':
            #     self.line_no += 1; # BAAAAD!!!!
            self.lex_char()
            self.offset += 1

        self.curr_char = 'EOF'
        self.lex_char()

        # if self.running:
        #     self.curr_char = '\n'
        #     self.lex_char()
        # if self.state != ':START':
        #     self.lexer_error(f'unterminated something {self.state}', None)

        if self.state == ':START':
            self.complete_token(':EOF')
        elif self.state == ':LIT_STR':
            self.error('unterminated string')
        else:
            self.error(f'unterminated token: {self.state}')

    def lex_char(self):
        if self.state == ':COMMENT_SL':
            self.lex_comment_sl()
        elif self.state == ':IDENT':
            self.lex_ident()
        elif self.state == ':LIT_INT':
            self.lex_lit_int()
        elif self.state == ':LIT_STR':
            self.lex_lit_str()
        elif self.state == ':LIT_STR_ESCAPE':
            self.lex_lit_str_escape()
        elif self.state == ':OP_L':
            self.lex_op_l()
        elif self.state == ':START':
            self.lex_start()
        else:
            raise Exception(f'bad state {self.state}')

    def lex_comment_sl(self):
        if self.curr_char == '\n':
            self.line_no += 1
            self.state = ':START'
        else:
            pass  # ignore

    def lex_ident(self):
        if self.curr_char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            self.add()
        elif self.curr_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            self.add()
        elif self.curr_char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.add()
        elif self.curr_char == '_':
            self.add()
        else:
            self.complete_ident()

    def lex_lit_int(self):
        if self.curr_char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.add()
        else:
            self.rewind()
            self.complete_token(':LIT_INT')

    def lex_lit_str(self):
        if self.curr_char == '"':
            self.complete_token(':LIT_STR')
        elif self.curr_char == '\\':
            self.state = ':LIT_STR_ESCAPE'
        elif self.curr_char == '\n':
            self.add()
            self.line_no += 1
        else:
            self.add()

    def lex_lit_str_escape(self):
        if self.curr_char == '"':
            # TODO pythonic syntax
            self.buffer += "\""
        elif self.curr_char == 't':
            self.buffer += "\t"
        elif self.curr_char == 'n':
            self.buffer += "\n"
        # TODO is it right
        elif self.curr_char == "\\":
            self.buffer += "\\"
        else:
            # self.lexer_error('invalid_escape symbol \\', self.curr_char)
            self.lexer_error('invalid_escape symbol', self.curr_char)
        self.state = ':LIT_STR'

    def lex_op_l(self):
        if self.curr_char == '=':
            self.complete_token(':OP_LE')
        else:
            self.rewind()
            self.complete_token(':OP_L')

    def lex_start(self):
        if self.curr_char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char == '_':
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.add()
            self.begin_token(':LIT_INT')  # FIX
        elif self.curr_char == '"':
            self.begin_token(':LIT_STR')
        elif self.curr_char == '#':
            self.state = ':COMMENT_SL'
        elif self.curr_char == ' ':
            pass  # ignore
        elif self.curr_char == '\n':
            self.line_no += 1
        elif self.curr_char == '\t':
            pass # ignore?
        elif self.curr_char == '+':
            self.begin_token(':START')
            self.complete_token(':OP_PLUS')
        elif self.curr_char == '<':
            self.begin_token(':OP_L') # delta = -1
        elif self.curr_char == '<':
            self.begin_token(':OP_G') # delta = -1
        elif self.curr_char == '=':
            self.begin_token(':START')
            self.complete_token(':OP_E')
        elif self.curr_char == '-':
            self.begin_token(':START')
            self.complete_token(':OP_SUB')
        elif self.curr_char == '*':
            self.begin_token(':START')
            self.complete_token(':OP_MUL')
        elif self.curr_char == '/':
            self.begin_token(':START')
            self.complete_token(':OP_DIV')
        elif self.curr_char == '(':
            self.begin_token(':START')
            self.complete_token(':OP_PAREN_O')
        elif self.curr_char == ')':
            self.begin_token(':START')
            self.complete_token(':OP_PAREN_C')
        elif self.curr_char == '{':
            self.begin_token(':START')
            self.complete_token(':OP_BRACE_O')
        elif self.curr_char == '}':
            self.begin_token(':START')
            self.complete_token(':OP_BRACE_C')
        elif self.curr_char == ';':
            self.begin_token(':START')
            self.complete_token(':OP_SEMICOLON')
        elif self.curr_char == ',':
            self.begin_token(':START')
            self.complete_token(':OP_COMMA')
        else:
            self.error()

    def error(self, msg=None):
        if not msg:
            msg = f'unexpected input character'

        self.lexer_error(msg, self.curr_char)
        self.running = False

    def lexer_error(self, msg, var_to_pprint):
        print(f'[program_name.fx]:{self.line_no}: lexer error: {msg}'),
        pprint(var_to_pprint)

    def rewind(self):
        self.offset -= 1
