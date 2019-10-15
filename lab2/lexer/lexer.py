from pprint import pprint

KEYWORDS = {
    'fx': 'KW_FN',
    'in': 'KW_FN_IN',
    'out': 'KW_FN_OUT',
    'if': 'KW_IF',
    'elif': 'KW_ELIF',
    'else': 'KW_ELSE',
    'for': 'KW_FOR',
    'while': 'KW_WHILE',
    'break': 'KW_BREAK',
    'continue': 'KW_CONTINUE',
    'return': 'KW_RETURN',
    '==>': 'KW_RET_ARROW',
    'void': 'KW_VOID',
    'int': 'KW_INT',
    'float': 'KW_FLOAT',
    'bool': 'KW_BOOL',
    'char': 'KW_CHAR',
    'string': 'KW_STRING',
    'struct': 'KW_STRUCT',
}

CONSTANTS = {
    'NULL': 'CONST_NULL',
    'True': 'CONST_TRUE',
    'False': 'CONST_FALSE',
}

OPERATORS = {
    'AND': 'OP_AND',
    'OR': 'OP_OR',
}


class Input:
    name: str
    text: str
    offset: int
    offset_prev: int
    pos: int
    curr_ln: int
    size: int

    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.size = len(text)
        self.curr_ln = 1
        self.offset = 0
        self.offset_prev = 0

    def read_char(self):
        char = self.text[self.offset]
        self.offset += 1
        return char

    def reverse_read(self, delta=1):
        self.offset -= delta

    def is_input_read(self):
        return self.offset >= self.size

    def next_line(self):
        self.offset_prev = self.offset
        self.curr_ln += 1


class Token:
    type_: str
    value: str
    line_no: int

    def __init__(self, type_, value, line_no):
        self.type = type_
        self.value = value
        self.line_no = line_no


class Lexer:
    inputs: list
    curr_input: Input
    buffer: str
    state: str
    tokens: list
    running: bool
    curr_char: str

    def __init__(self, inputs) -> None:
        if type(inputs) == list:
            self.inputs = [inputs]
        elif type(inputs) == Input:
            self.inputs = [inputs]
        else:
            self.lexer_error('Wrong input passed to lexer constructor.')

        self.buffer = ''
        self.offset = 0
        self.state = 'START'
        self.tokens = []
        self.token_start_ln = 1
        self.running = True
        self.curr_char = ''

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.token_start_ln = self.curr_input.curr_ln
        self.state = new_state

    def complete_ident(self):
        self.curr_input.reverse_read()

        if self.buffer in KEYWORDS:
            token_type = KEYWORDS[self.buffer]
            self.buffer = ''
        elif self.buffer in CONSTANTS:
            token_type = CONSTANTS[self.buffer]
            self.buffer = ''
        elif self.buffer in OPERATORS:
            token_type = OPERATORS[self.buffer]
            self.buffer = ''
        else:
            token_type = 'IDENT'

        self.complete_token(token_type)

    def complete_token(self, token_type, reverse=False, delta=0):
        self.tokens.append(
            Token(token_type, self.buffer, self.token_start_ln))
        self.buffer = ''
        self.state = 'START'
        if reverse:
            self.curr_input.reverse_read(delta)

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<14} | {"VALUE":<14}')
        for index, token in enumerate(self.tokens):
            print(f'{index:>3}|'
                  f' {token.line_no:>3}|'
                  f' {token.type:<14} |'
                  f' {token.value:<14}')

    def lex_all(self):

        for _input in self.inputs:
            self.curr_input = _input

            # uncomment for debugging
            print(81 * '#')
            pprint(self.curr_input.text)
            print(81 * '#')

            while self.running and not self.curr_input.is_input_read():
                self.curr_char = self.curr_input.read_char()
                self.lex_char()

            self.curr_char = 'EOF'

            if self.state == 'START':
                self.complete_token('EOF')
            else:
                self.lex_char()

            if self.state == 'LIT_STR':
                self.lexer_error('unterminated string')
            # elif self.state == 'LIT_CHAR':
            #     self.lexer_error('unterminated char')
            # else:
            #     self.lexer_error(f'unterminated token: {self.state}')

            # if self.running:
            #     self.curr_char = '\n'
            #     self.lex_char()
            # if self.state != 'START'
            #     self.lexer_error(f'unterminated token: {self.state}')

    def lex_char(self):
        if self.state == 'COMMENT_SL':
            self.lex_comment_sl()
        elif self.state == 'IDENT':
            self.lex_ident()
        elif self.state == 'LIT_INT':
            self.lex_lit_int()
        elif self.state == 'LIT_FLOAT':
            self.lex_lit_float()
        elif self.state == 'LIT_FLOAT_E':
            self.lex_lit_float_e()
        elif self.state == 'LIT_FLOAT_W_E':
            self.lex_lit_float_w_e()
        elif self.state == 'LIT_CHAR':
            self.lex_lit_char()
        elif self.state == 'LIT_CHAR_ESCAPE':
            self.lex_lit_char_escape()
        elif self.state == 'LIT_CHAR_ADDED':
            self.lex_lit_char_added()
        elif self.state == 'LIT_STR':
            self.lex_lit_str()
        elif self.state == 'LIT_STR_ESCAPE':
            self.lex_lit_str_escape()
        elif self.state == 'OP_L':
            self.lex_op_l()
        elif self.state == 'OP_G':
            self.lex_op_g()
        elif self.state == 'OP_EXCL':
            self.lex_op_excl()
        elif self.state == 'OP_ASSIGN_EQ':
            self.lex_op_assign_eq()


        elif self.state == 'START':
            self.lex_start()
        else:
            raise self.lexer_error(f'invalid state {self.state}')

    def lex_comment_sl(self):
        if self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'START'
        else:
            pass  # ignore

    def lex_ident(self):
        if self.is_letter():
            self.add()
        elif self.is_digit():
            self.add()
        elif self.curr_char == '_':
            self.add()
        else:
            self.complete_ident()

    def lex_lit_int(self):
        if self.is_digit():
            self.add()
        elif self.curr_char == '.':
            self.add()
            self.state = 'LIT_FLOAT'
        else:
            self.curr_input.reverse_read()
            self.complete_token('LIT_INT')

    def lex_lit_float(self):
        if self.is_digit():
            self.add()
        elif self.curr_char == 'e':
            self.add()
            self.state = 'LIT_FLOAT_E'
        else:
            self.curr_input.reverse_read()
            self.complete_token('LIT_FLOAT')

    def lex_lit_float_e(self):
        if self.is_digit():
            self.add()
            self.state = 'LIT_FLOAT_W_E'
        elif self.curr_char in ['+', '-']:
            self.add()
        else:
            self.lexer_error('Float exponent cannot be empty')

    def lex_lit_float_w_e(self):
        if self.is_digit():
            self.add()
        else:
            self.curr_input.reverse_read()
            self.complete_token('LIT_FLOAT')

    def lex_lit_char(self):
        if self.curr_char == '\'':
            self.complete_token('LIT_CHAR')
        elif self.curr_char == '\\':
            self.state = 'LIT_CHAR_ESCAPE'
        elif self.curr_char in ['\n', '\r', '\t']:
            self.lexer_error('char type cannot contain newlines, tabstops or'
                             ' carriage returns', self.buffer + self.curr_char)
        else:
            self.add()
            self.state = 'LIT_CHAR_ADDED'

    def lex_lit_char_escape(self):
        if self.curr_char == '\'':
            self.buffer += '\''
        elif self.curr_char == '\\':
            self.buffer += '\\'
        elif self.curr_char == 'n':
            self.buffer += '\\n'
        elif self.curr_char == 'r':
            self.buffer += '\\r'
        elif self.curr_char == 't':
            self.buffer += '\\t'
        self.state = 'LIT_CHAR_ADDED'

    def lex_lit_char_added(self):
        if self.curr_char == '\'':
            self.complete_token('LIT_CHAR')
        else:
            self.lexer_error('char type cannot consist of multiple chars', self.buffer + self.curr_char)

    def lex_lit_str(self):
        if self.curr_char == '"':
            self.complete_token('LIT_STR')
        elif self.curr_char == '\\':
            self.state = 'LIT_STR_ESCAPE'
        elif self.curr_char == '\n':
            self.add()
            self.curr_input.next_line()
        else:
            self.add()

    def lex_lit_str_escape(self):
        if self.curr_char == '"':
            self.buffer += '"'
        elif self.curr_char == "\\":
            self.buffer += "\\"
        elif self.curr_char == 'n':
            self.buffer += "\\n"
        elif self.curr_char == 'r':
            self.buffer += "\\r"
        elif self.curr_char == 't':
            self.buffer += "\\t"
        else:
            self.buffer += "\\"
            self.curr_input.reverse_read()
        self.state = 'LIT_STR'

    def lex_op_l(self):
        if self.curr_char == '=':
            self.complete_token('OP_LE')
        else:
            self.curr_input.reverse_read()
            self.complete_token('OP_L')

    def lex_op_g(self):
        if self.curr_char == '=':
            self.complete_token('OP_GE')
        else:
            self.curr_input.reverse_read()
            self.complete_token('OP_G')

    def lex_op_excl(self):
        if self.curr_char == '=':
            self.buffer = ''
            self.complete_token('OP_IS_NEQ')
        else:
            self.curr_input.reverse_read()
            self.complete_token('OP_EXCL')

    def lex_op_assign_eq(self):
        if self.curr_char == '=':
            self.buffer = ''
            self.complete_token('OP_IS_EQ')
        else:
            self.curr_input.reverse_read()
            self.buffer = ''
            self.complete_token('OP_ASSIGN_EQ')

    def lex_start(self):
        if self.is_letter():
            self.add()
            self.begin_token('IDENT')
        elif self.curr_char == '_':
            self.add()
            self.begin_token('IDENT')
        elif self.is_digit():
            self.add()
            self.begin_token('LIT_INT')
        elif self.curr_char == '.':
            self.add()
            self.begin_token('LIT_FLOAT')
        elif self.curr_char == '\'':
            self.begin_token('LIT_CHAR')
        elif self.curr_char == '"':
            self.begin_token('LIT_STR')
        elif self.curr_char == '#':
            self.state = 'COMMENT_SL'
        elif self.curr_char == ' ':
            pass  # ignore
        elif self.curr_char == '\n':
            self.curr_input.next_line()
        elif self.curr_char == '\t':
            pass  # ignore
        elif self.curr_char == '+':
            self.begin_token('START')
            self.complete_token('OP_SUM')
        elif self.curr_char == '<':
            self.begin_token('OP_L')
        elif self.curr_char == '>':
            self.begin_token('OP_G')
        elif self.curr_char == '-':
            self.begin_token('START')
            self.complete_token('OP_SUB')
        elif self.curr_char == '*':
            self.begin_token('START')
            self.complete_token('OP_MUL')
        elif self.curr_char == '/':
            self.begin_token('START')
            self.complete_token('OP_DIV')
        elif self.curr_char == '%':
            self.begin_token('START')
            self.complete_token('OP_MOD')
        elif self.curr_char == '(':
            self.begin_token('START')
            self.complete_token('OP_PAREN_O')
        elif self.curr_char == ')':
            self.begin_token('START')
            self.complete_token('OP_PAREN_C')
        elif self.curr_char == '{':
            self.begin_token('START')
            self.complete_token('OP_BRACE_O')
        elif self.curr_char == '}':
            self.begin_token('START')
            self.complete_token('OP_BRACE_C')
        elif self.curr_char == '[':
            self.begin_token('START')
            self.complete_token('OP_BRACKET_O')
        elif self.curr_char == ']':
            self.begin_token('START')
            self.complete_token('OP_BRACKET_C')
        elif self.curr_char == ';':
            self.begin_token('START')
            self.complete_token('OP_SEMICOLON')
        elif self.curr_char == ',':
            self.begin_token('START')
            self.complete_token('OP_COMMA')
        elif self.curr_char == '!':
            self.add()
            self.begin_token('OP_EXCL')
        elif self.curr_char == '=':
            self.add()
            self.begin_token('OP_ASSIGN_EQ')
        else:
            self.lexer_error(item=self.curr_char)

    def is_letter(self):
        c = self.curr_char
        return len(c) == 1 and (ord(c) in range(ord('A'), ord('Z') + 1) or ord(c) in range(ord('a'), ord('z') + 1))

    def is_digit(self):
        return len(self.curr_char) == 1 and ord(self.curr_char) in range(ord('0'), ord('9') + 1)

    def lexer_error(self, msg=None, item=None):
        top_right_delim = 33 * '!'
        top_left_delim = 33 * '!'
        v_delim = 5 * '!'
        bottom_delim = 81 * '!'

        print(f'{top_left_delim} [Lexer error] {top_right_delim}')
        print(f'{v_delim} [@] [inputName: {self.curr_input.name} '
              f'line: {self.curr_input.curr_ln} '
              f'position: {self.curr_input.offset - self.curr_input.offset_prev}]')
        if not msg:
            msg = 'Something went wrong'
        print(f'{v_delim} [Error message]: {msg}'),
        if item:
            print(f'{v_delim} [Item being lexed]:'),
            pprint(item)
        print(f'{v_delim} [state]: {self.state}')
        print(f'{v_delim} [output so far]:')
        self.dump_tokens()
        print(bottom_delim)
        exit(1)

    def debug(self, msg=None):
        self.dump_tokens()
        print(self.buffer)
        print(self.state)
        print(msg)
        exit(1)
