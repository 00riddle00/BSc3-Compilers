from pprint import pprint
from errors import LexerError, LexerDebugError, InputError

# List of all lexemes

# <KW_INCLUDE> // not implemented
# <KW_FN>
# <KW_FN_RET_ARROW>
# <KW_FN_IN>
# <KW_FN_OUT>
# <KW_IF>
# <KW_ELIF>
# <KW_ELSE>
# <KW_FOR>
# <KW_WHILE>
# <KW_BREAK>
# <KW_CONTINUE>
# <KW_RETURN>
# <KW_VOID>
# <KW_INT>
# <KW_FLOAT>
# <KW_BOOL>
# <KW_CHAR>
# <KW_STR>
# <KW_STRUCT>
# <KW_NULL>
# <KW_TRUE>
# <KW_FALSE>
# <KW_AND>
# <KW_OR>

# <IDENT>

# <LIT_INT>
# <LIT_FLOAT>
# <LIT_CHAR>
# <LIT_STR>

# <OP_G>
# <OP_GE>
# <OP_L>
# <OP_LE>
# <OP_IS_EQ>
# <OP_IS_NEQ>

# <OP_SUM>
# <OP_SUB>
# <OP_MUL>
# <OP_DIV>
# <OP_MOD>
# <OP_NOT>
# <OP_INCR>
# <OP_DECR>

# <OP_ASSIGN_EQ>
# <OP_ASSIGN_SUM>
# <OP_ASSIGN_SUB>
# <OP_ASSIGN_MUL>
# <OP_ASSIGN_DIV>
# <OP_ASSIGN_MOD>

# <OP_PTR>
# <OP_PTR_ADDR>

# <OP_DOT_ACCESS_MEMBER>
# <OP_PTR_ACCESS_MEMBER> // not implemented

# <OP_PAREN_O>
# <OP_PAREN_C>
# <OP_BRACE_O>
# <OP_BRACE_C>
# <OP_BRACKET_O>
# <OP_BRACKET_C>
# <OP_SEMICOLON>
# <OP_COMMA>

KEYWORDS = {
    'fx': 'KW_FN',
    # 'in': 'KW_FN_IN',  # see this inbuilt fn name just as ident
    # 'out': 'KW_FN_OUT', # see this inbuilt fn name just as ident
    'if': 'KW_IF',
    'elif': 'KW_ELIF',
    'else': 'KW_ELSE',
    'for': 'KW_FOR',
    'while': 'KW_WHILE',
    'break': 'KW_BREAK',
    'continue': 'KW_CONTINUE',
    'return': 'KW_RETURN',
    '==>': 'KW_FN_RET_ARROW',
    'void': 'KW_VOID',
    'int': 'KW_INT',
    'float': 'KW_FLOAT',
    'bool': 'KW_BOOL',
    'char': 'KW_CHAR',
    'string': 'KW_STR',
    'struct': 'KW_STRUCT',
    'NULL': 'KW_NULL',
    'True': 'KW_TRUE',
    'False': 'KW_FALSE',
    'AND': 'KW_AND',
    'OR': 'KW_OR',
}


class Input:
    name: str
    text: str
    offset: int
    offset_prev_line: int
    offset_token_start: int
    pos: int
    curr_ln: int
    size: int

    def __init__(self, filename):
        if not type(filename) == str:
            raise InputError(f"Wrong argument type passed to Input constructor: exp=str, got={type(filename)}")
        self.name = filename
        try:
            with open(self.name) as f:
                self.text = ''.join(f.readlines())
        except IOError as e:
            raise InputError(e)
        self.size = len(self.text)
        self.curr_ln = 1
        self.offset = 0
        self.offset_prev_line = 0
        self.offset_token_start = 0

    def read_char(self):
        char = self.text[self.offset]
        self.offset += 1
        return char

    def reverse_read(self, delta=1):
        self.offset -= delta

    def is_input_read(self):
        return self.offset >= self.size

    def next_line(self):
        self.offset_prev_line = self.offset
        self.curr_ln += 1
        self.offset_token_start = 0

    def get_char_pos(self):
        return self.offset - self.offset_prev_line

    def get_info(self):
        return [self.name, self.curr_ln, self.get_char_pos()]


class Token:
    type_: str
    value: str
    file: str
    line_no: int
    pos: int

    def __init__(self, type_, value, file, line_no, pos):
        self.type = type_
        self.value = value
        self.file = file
        self.line_no = line_no
        self.pos = pos

    def get_info(self):
        return [self.file, self.line_no, self.pos]


class Lexer:
    inputs: list
    curr_input: Input
    buffer: str
    state: str
    tokens: list
    running: bool
    curr_char: str

    def __init__(self, inputs) -> None:
        if not type(inputs) == list:
            self.err(
                f"Wrong argument type passed to Lexer constructor: exp=[Input, Input, ...], got={type(inputs)}")
        for i, _input in enumerate(inputs):
            if not type(_input) == Input:
                self.err(
                    f'Input list has an element (index={i}) of incorrect type: exp=Input, got={type(_input)}')
        self.inputs = inputs

        self.buffer = ''
        self.state = 'START'
        self.tokens = []
        self.token_start_ln = 1
        self.running = True
        self.curr_char = ''

    def add(self):
        self.buffer += self.curr_char

    def begin_token(self, new_state):
        self.curr_input.offset_token_start = self.curr_input.get_char_pos()
        self.token_start_ln = self.curr_input.curr_ln
        self.state = new_state

    def complete_ident(self):

        if self.buffer in KEYWORDS:
            token_type = KEYWORDS[self.buffer]
            self.buffer = ''
        else:
            token_type = 'IDENT'

        self.complete_token(token_type, delta=1)

    def complete_at_once(self, token_type):
        self.curr_input.offset_token_start = self.curr_input.get_char_pos()
        self.complete_token(token_type)

    def complete_token(self, token_type, delta=0):
        self.tokens.append(
            Token(token_type, self.buffer, self.curr_input.name, self.curr_input.curr_ln,
                  self.curr_input.offset_token_start))
        self.buffer = ''
        self.state = 'START'
        if delta:
            self.curr_input.reverse_read(delta)

    def dump_tokens(self):
        print(f'{"ID":>3}| {"LN":>3}| {"TYPE":<22} | {"VALUE":<14}')
        for index, token in enumerate(self.tokens):
            print(f'{index:>3}|'
                  f' {token.line_no:>3}|'
                  f' {token.type:<22} |'
                  f' {token.value:<14}')

    def lex_all(self):

        for _input in self.inputs:
            self.curr_input = _input

            # uncomment for debugging
            # print(81 * '#')
            # print(f'[file]: {self.curr_input.name}')
            # pprint(self.curr_input.text)
            # print(81 * '#')

            while self.running and not self.curr_input.is_input_read():
                self.curr_char = self.curr_input.read_char()
                self.lex_char()

            self.curr_char = 'EOF'

            if self.state == 'START':
                self.complete_at_once('EOF')
            elif self.state in ('COMMENT_ML', 'COMMENT_ML_MINUS_1', 'COMMENT_ML_MINUS_2'):
                self.err('unterminated comment')
            elif self.state in ('LIT_FLOAT_E', 'LIT_FLOAT_E_SIGN'):
                self.err('unterminated float expression')
            elif self.state in ('LIT_CHAR', 'LIT_CHAR_ADDED'):
                self.err('unterminated char')
            elif self.state == 'LIT_STR':
                self.err('unterminated string')
            elif self.state in ('LIT_CHAR_ESC', 'LIT_STR_ESCAPE'):
                self.err('unterminated escape symbol')
            else:
                self.lex_char()
                self.complete_at_once('EOF')

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
        elif self.curr_char == "'":
            self.begin_token('LIT_CHAR')
        elif self.curr_char == '"':
            self.begin_token('LIT_STR')
        elif self.curr_char == '#':
            self.state = 'COMMENT_START'
        elif self.curr_char == ' ':
            pass  # ignore
        elif self.curr_char == '\n':
            self.curr_input.next_line()
        elif self.curr_char == '\t':
            pass  # ignore
        elif self.curr_char == '\r':
            pass  # ignore
        elif self.curr_char == '<':
            self.begin_token('OP_L')
        elif self.curr_char == '>':
            self.begin_token('OP_G')
        elif self.curr_char == '+':
            self.begin_token('OP_SUM')
        elif self.curr_char == '-':
            self.begin_token('OP_SUB')
        elif self.curr_char == '*':
            self.begin_token('OP_MUL')
        elif self.curr_char == '/':
            self.begin_token('OP_DIV')
        elif self.curr_char == '%':
            self.begin_token('OP_MOD')
        elif self.curr_char == '=':
            self.begin_token('OP_ASSIGN_EQ')
        elif self.curr_char == '!':
            self.begin_token('OP_NOT')
        elif self.curr_char == '(':
            self.complete_at_once('OP_PAREN_O')
        elif self.curr_char == ')':
            self.complete_at_once('OP_PAREN_C')
        elif self.curr_char == '{':
            self.complete_at_once('OP_BRACE_O')
        elif self.curr_char == '}':
            self.complete_at_once('OP_BRACE_C')
        elif self.curr_char == '[':
            self.complete_at_once('OP_BRACKET_O')
        elif self.curr_char == ']':
            self.begin_token('OP_BRACKET_C')
        elif self.curr_char == ';':
            self.complete_at_once('OP_SEMICOLON')
        elif self.curr_char == ',':
            self.complete_at_once('OP_COMMA')
        elif self.curr_char == '$':
            self.complete_at_once('OP_PTR')
        elif self.curr_char == '&':
            self.complete_at_once('OP_PTR_ADDR')
        elif self.curr_char == '@':
            self.begin_token('INCLUDE')
        else:
            self.err('invalid character, usable only as char or inside a string')

    def lex_char(self):
        if self.state == 'COMMENT_START':
            self.lex_comment_start()
        if self.state == 'COMMENT_SL':
            self.lex_comment_sl()
        elif self.state == 'COMMENT_SL_PLUS_2':
            self.lex_comment_sl_plus_2()
        elif self.state == 'COMMENT_ML':
            self.lex_comment_ml()
        elif self.state == 'COMMENT_ML_MINUS_1':
            self.lex_comment_ml_minus_1()
        elif self.state == 'COMMENT_ML_MINUS_2':
            self.lex_comment_ml_minus_2()
        elif self.state == 'IDENT':
            self.lex_ident()
        elif self.state == 'LIT_INT':
            self.lex_lit_int()
        elif self.state == 'LIT_FLOAT':
            self.lex_lit_float()
        elif self.state == 'LIT_FLOAT_E':
            self.lex_lit_float_e()
        elif self.state == 'LIT_FLOAT_E_SIGN':
            self.lex_lit_float_e_sign()
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
        elif self.state == 'OP_BRACKET_C':
            self.lex_op_bracket_close()
        elif self.state == 'OP_PAREN_C':
            self.lex_op_paren_close()
        elif self.state == 'OP_L':
            self.lex_op_l()
        elif self.state == 'OP_G':
            self.lex_op_g()
        elif self.state == 'OP_SUM':
            self.lex_op_sum()
        elif self.state == 'OP_SUB':
            self.lex_op_sub()
        elif self.state == 'OP_MUL':
            self.lex_op_mul()
        elif self.state == 'OP_DIV':
            self.lex_op_div()
        elif self.state == 'OP_MOD':
            self.lex_op_mod()
        elif self.state == 'OP_ASSIGN_EQ':
            self.lex_op_assign_eq()
        elif self.state == 'OP_IS_EQ':
            self.lex_op_is_eq()
        elif self.state == 'OP_NOT':
            self.lex_op_not()
        elif self.state == 'STRUCT_MEMBER':
            self.lex_struct_member()
        elif self.state == 'START':
            self.lex_start()
        elif self.state == 'INCLUDE':
            self.lex_include()
        else:
            self.err(f'invalid state {self.state}')

    def lex_comment_start(self):
        if self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'START'
        elif self.curr_char == '#':
            self.state = 'COMMENT_SL_PLUS_2'
        else:
            self.state = 'COMMENT_SL'

    def lex_comment_sl(self):
        if self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'START'
        else:
            pass  # ignore

    def lex_comment_sl_plus_2(self):
        if self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'START'
        elif self.curr_char == '#':
            self.state = 'COMMENT_ML'
        else:
            self.state = 'COMMENT_SL'

    def lex_comment_ml(self):
        if self.curr_char == '#':
            self.state = 'COMMENT_ML_MINUS_1'
        elif self.curr_char == '\n':
            self.curr_input.next_line()
        else:
            pass  # ignore

    def lex_comment_ml_minus_1(self):
        if self.curr_char == '#':
            self.state = 'COMMENT_ML_MINUS_2'
        elif self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'COMMENT_ML'
        else:
            self.state = 'COMMENT_ML'

    def lex_comment_ml_minus_2(self):
        if self.curr_char == '#':
            self.state = 'START'
        elif self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'COMMENT_ML'
        else:
            self.state = 'COMMENT_ML'

    def lex_ident(self):
        if self.is_letter():
            self.add()
        elif self.is_digit():
            self.add()
        elif self.curr_char == '_':
            self.add()
        elif self.curr_char == '.':
            self.complete_token('IDENT')
            self.add()
            self.state = 'STRUCT_MEMBER'
        else:
            self.complete_ident()

    def lex_op_bracket_close(self):
        self.complete_token('OP_BRACKET_C')
        if self.curr_char == '.':
            self.add()
            self.state = 'STRUCT_MEMBER'

    def lex_op_paren_close(self):
        self.complete_token('OP_PAREN_C')
        if self.curr_char == '.':
            self.add()
            self.state = 'STRUCT_MEMBER'

    def lex_struct_member(self):
        if self.is_ident_head():
            self.complete_token('OP_DOT_ACCESS_MEMBER')
            self.add()
            self.state = 'IDENT'
        else:
            self.err('invalid struct member ident')

    def lex_lit_int(self):
        if self.is_digit():
            self.add()
        elif self.curr_char == '.':
            self.add()
            self.state = 'LIT_FLOAT'
        elif self.is_ident_head():
            self.err('invalid int suffix')
        else:
            self.complete_token('LIT_INT', delta=1)

    def lex_lit_float(self):
        if self.is_digit():
            self.add()
        elif self.curr_char == 'e':
            self.add()
            self.state = 'LIT_FLOAT_E'
        else:
            self.complete_token('LIT_FLOAT', delta=1)

    def lex_lit_float_e(self):
        if self.is_digit():
            self.add()
            self.state = 'LIT_FLOAT_W_E'
        elif self.curr_char in ['+', '-']:
            self.add()
            self.state = 'LIT_FLOAT_E_SIGN'
        else:
            self.err('Invalid float exponent')

    def lex_lit_float_e_sign(self):
        if self.is_digit():
            self.add()
            self.state = 'LIT_FLOAT_W_E'
        else:
            self.err('Invalid float exponent')

    def lex_lit_float_w_e(self):
        if self.is_digit():
            self.add()
        else:
            self.complete_token('LIT_FLOAT', delta=1)

    def lex_lit_char(self):
        if self.curr_char == "'":
            self.complete_token('LIT_CHAR')
        elif self.curr_char == '\\':
            self.state = 'LIT_CHAR_ESCAPE'
        elif self.curr_char in ['\n', '\r', '\t']:
            self.err('char type cannot contain newlines, tabstops or'
                     ' carriage returns')
        else:
            self.add()
            self.state = 'LIT_CHAR_ADDED'

    def lex_lit_char_escape(self):
        if self.curr_char == "'":
            self.buffer += "'"
        elif self.curr_char == '\\':
            self.buffer += '\\'
        elif self.curr_char == 'n':
            self.buffer += '\\n'
        elif self.curr_char == 'r':
            self.buffer += '\\r'
        elif self.curr_char == 't':
            self.buffer += '\\t'
        else:
            self.buffer += "\\"
            self.err(f'invalid escape sequence used in a char: \\{self.curr_char}')
        self.state = 'LIT_CHAR_ADDED'

    def lex_lit_char_added(self):
        if self.curr_char == "'":
            self.complete_token('LIT_CHAR')
        else:
            self.err('char type cannot consist of multiple chars')

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
            self.buffer += "\n"
        elif self.curr_char == 'r':
            self.buffer += "\r"
        elif self.curr_char == 't':
            self.buffer += "\t"
        else:
            self.buffer += "\\"
            self.err(f'invalid escape sequence used in a string: \\{self.curr_char}')
        self.state = 'LIT_STR'

    def lex_op_l(self):
        if self.curr_char == '=':
            self.complete_token('OP_LE')
        else:
            self.complete_token('OP_L', delta=1)

    def lex_op_g(self):
        if self.curr_char == '=':
            self.complete_token('OP_GE')
        else:
            self.complete_token('OP_G', delta=1)

    def lex_op_sum(self):
        if self.curr_char == '+':
            self.complete_token('OP_INCR')
        elif self.curr_char == '=':
            self.complete_token('OP_ASSIGN_SUM')
        elif self.is_digit():
            self.add()
            self.state = 'LIT_INT'
        else:
            self.complete_token('OP_SUM', delta=1)

    def lex_op_sub(self):
        if self.curr_char == '-':
            self.complete_token('OP_DECR')
        elif self.curr_char == '=':
            self.complete_token('OP_ASSIGN_SUB')
        elif self.is_digit():
            self.add()
            self.state = 'LIT_INT'
        else:
            self.buffer = ''
            self.complete_token('OP_SUB', delta=1)

    def lex_op_mul(self):
        if self.curr_char == '=':
            self.complete_token('OP_ASSIGN_MUL')
        else:
            self.complete_token('OP_MUL', delta=1)

    def lex_op_div(self):
        if self.curr_char == '=':
            self.complete_token('OP_ASSIGN_DIV')
        else:
            self.complete_token('OP_DIV', delta=1)

    def lex_op_mod(self):
        if self.curr_char == '=':
            self.complete_token('OP_ASSIGN_MOD')
        else:
            self.complete_token('OP_MOD', delta=1)

    def lex_op_assign_eq(self):
        if self.curr_char == '=':
            self.state = 'OP_IS_EQ'
        else:
            self.complete_token('OP_ASSIGN_EQ', delta=1)

    def lex_op_is_eq(self):
        if self.curr_char == '>':
            self.complete_token(KEYWORDS['==>'])
        else:
            self.complete_token('OP_IS_EQ', delta=1)

    def lex_op_not(self):
        if self.curr_char == '=':
            self.complete_token('OP_IS_NEQ')
        else:
            self.complete_token('OP_NOT', delta=1)

    def lex_include(self):
        if self.curr_char == '\n':
            self.curr_input.next_line()
            self.state = 'START'
            new_input = Input(self.buffer)
            self.buffer = ''
            self.inputs.append(new_input)
        else:
            self.add()

    def is_letter(self):
        c = self.curr_char
        return len(c) == 1 and (ord(c) in range(ord('A'), ord('Z') + 1) or ord(c) in range(ord('a'), ord('z') + 1))

    def is_ident_head(self):
        if self.curr_char == '_':
            return True
        c = self.curr_char
        return len(c) == 1 and (ord(c) in range(ord('A'), ord('Z') + 1) or ord(c) in range(ord('a'), ord('z') + 1))

    def is_digit(self):
        return len(self.curr_char) == 1 and ord(self.curr_char) in range(ord('0'), ord('9') + 1)

    def err(self, msg, debug=False):
        if debug:
            raise LexerDebugError(msg, *self.curr_input.get_info(), self.state, self.curr_char, self.buffer)
        else:
            raise LexerError(msg, *self.curr_input.get_info())
