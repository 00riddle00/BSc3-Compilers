

keywords = {
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

        assert len(_input)

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.token_start = self.line_no
        self.state = new_state

    def complete_ident(self):
        if kw_type == keywords[self.buffer]:
            self.buffer = ''
            self.complete_token(kw_type, False)
        else:
            self.complete_token(':IDENT', False)

    def complete_token(self, token_type, advance = True):
        self.tokens.append(Token(token_type, self.buffer, self.token_start))
        # print(f'token: {token_type} {self.buffer}')
        self.buffer = ''
        state = ':START'
        if not advance:
            self.offset -= 1

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<10} | {"VALUE":<10}')
        for index, token in enumerate(self.token):
            print(f'{index:>3}| {token.line_no:>3}| {token.type:<10} | {token.value:<10}')

    def error(self, msg = None):
        if not msg:
            msg = f'unexpected input character {self.curr_char}'

        print(f'sample.fx:{self.line_no} lexer error: {msg}')
        self.running = False

    def lex_all(self):
            try:
                while self.offset < len(self._input):
                    pass

            except BufferError as e:
                print(str(e))
                raise ValueError()

            return self.tokens

    def print_tokens(self):
        print("TEST")
        pass









