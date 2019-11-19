from pprint import pprint
from lexer import Lexer


class ParserError(BaseException):
    # parser: Parser

    def __init__(self, parser, msg=None, expected_token=None):
        self.parser = parser
        self.expected_token = expected_token
        self.msg = msg

    def print_err(self):
        top_right_delim = 33 * '!'
        top_left_delim = 33 * '!'
        v_delim = 5 * '!'
        bottom_delim = 81 * '!'

        print(f'{top_left_delim} [Lexer error] {top_right_delim}')
        print(f'{v_delim} [file={self.parser.curr_input.name}:'
              f'line={self.parser.curr_input.curr_ln}:',
              f'position={self.parser.curr_input.offset - self.parser.curr_input.offset_prev}]')

        print(f'{v_delim} [Error message]: expected={self.expected_token}, found={self.parser.curr_token.type}')
        print(f'{v_delim} [Error details]: {self.msg}'),
        # if self.buffer:
        #     print(f'{v_delim} [Item being parsed (pretty print)]:'),
        # pprint(buffer)
        # print(f'{v_delim} [state]: {self.state}')
        # print(f'{v_delim} [output so far]:')
        # self.dump_tokens()
        print(bottom_delim)


class LexerError(BaseException):
    lexer: Lexer

    def __init__(self, lexer, msg=None, is_buffer=False):
        self.lexer = lexer
        self.msg = msg
        self.is_buffer = is_buffer

    def print_err(self):
        top_right_delim = 33 * '!'
        top_left_delim = 33 * '!'
        v_delim = 5 * '!'
        bottom_delim = 81 * '!'

        print(f'{top_left_delim} [Lexer error] {top_right_delim}')
        print(f'{v_delim} [file={self.lexer.curr_input.name}:'
              f'line={self.lexer.curr_input.curr_ln}:',
              f'position={self.lexer.curr_input.offset - self.lexer.curr_input.offset_prev}]')

        if not self.msg:
            self.msg = 'Something went wrong'
        print(f'{v_delim} [Error message]: {self.msg}'),
        if self.is_buffer:
            print(f'{v_delim} [Item being lexed (pretty print)]:'),
            pprint(self.lexer.buffer + self.lexer.curr_char)
        print(f'{v_delim} [state]: {self.lexer.state}')
        print(f'{v_delim} [output so far]:')
        self.lexer.dump_tokens()
        print(bottom_delim)
