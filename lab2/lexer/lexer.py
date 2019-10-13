
KEYWORDS = {
  'if': ':KW_IF',
  'return': ':KW_RETURN',
  'while': ':KW_WHILE',
}


class Token:

    type_: str
    value: str
    line_no: int

    def __init__(self, type_, value, line_no):
        self.type = type
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
    running: bool
    curr_char: str

    def __init__(self, _input) -> None:
        self.buffer = ''

        self._input = _input
        # self._input = '2+3'

        self.line_no = 1

        self.offset = 0
        # self.offset = 4

        self.state = ':START'

        self.tokens = []
        # self.tokens = ['2', '+', '3']

        self.token_start = 0

        self.running = True

        self.curr_char = ''

        assert len(_input)

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.token_start = self.line_no
        self.state = new_state

    def complete_ident(self):
        if self.buffer in KEYWORDS:
            kw_type = KEYWORDS[self.buffer]
            self.buffer = ''
            self.complete_token(kw_type, False)
        else:
            self.complete_token(':IDENT', False)

    def complete_token(self, token_type, advance=True):
        self.tokens.append(Token(token_type, self.buffer, self.token_start))
        # print(f'token: {token_type} {self.buffer}')
        self.buffer = ''
        self.state = ':START'
        if not advance:
            self.offset -= 1

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<10} | {"VALUE":<10}')
        for index, token in enumerate(self.tokens):
            print(f'{index:>3}| {token.line_no:>3}| {token.type:<10} | {token.value:<10}')

    def error(self, msg=None):
        if not msg:
            msg = f'unexpected input character {self.curr_char}'

        print(f'sample.fx:{self.line_no} lexer error: {msg}')
        self.running = False

    def lex_all(self):
        while self.offset and self.offset < len(self._input):
            self.curr_char = self._input[self.offset]
            # if self.curr_char == '\n':
            #     self.line_no += 1; # BAAAAD!!!!
            self.offset += 1
            self.lex_char()
            self.offset += 1

        self.curr_char = 'EOF'
        self.lex_char()

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
        # TODO regexp
        if self.curr_char in ['a', 'z']:
            self.add()
        elif self.curr_char in ['A', 'Z']:
            self.add()
        elif self.curr_char in ['0', '9']:
            self.add()
        elif self.curr_char == '_':
            self.add()
        else:
            self.complete_ident()

    def lex_lit_int(self):
        # TODO regexp
        if self.curr_char in ['0', '9']:
            self.add()
        else:
            self.complete_token(':LIT_INT', False)

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
            self.buffer += "\""
        elif self.curr_char == 't':
            self.buffer += "\t"
        elif self.curr_char == 'n':
            self.buffer += "\n"
        else:
            self.error(f'invalid escape sequence "\\{self.curr_char}"')
        self.state = ':LIT_STR'

    def lex_op_l(self):
        if self.curr_char == '=':
            self.complete_token(':OP_LE')
        else:
            self.complete_token(':OP_L', False)

    def lex_start(self):
        # TODO regexp
        if self.curr_char in ['a', 'z']:
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char in ['A', 'Z']:
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char == '_':
            self.add()
            self.begin_token(':IDENT')
        elif self.curr_char in ['0', '9']:
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
        elif self.curr_char == '+':
            self.begin_token(':START')
            self.complete_token(':OP_PLUS')
        elif self.curr_char == '<':
            self.begin_token(':OP_L')
        elif self.curr_char == '=':
            self.begin_token(':START')
            self.complete_token(':OP_E')
        else:
            self.error()
