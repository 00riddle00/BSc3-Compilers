from abc import abstractmethod
from pprint import pprint


class CompilerError(BaseException):

    def __init__(self, msg, file=None, line=None, pos=None):
        self.msg = msg
        self.file = file
        self.line = line
        self.pos = pos

    @abstractmethod
    def print_err(self):
        pass


class InputError(CompilerError):

    def print_err(self):
        print(f'[InputERROR] [{self.msg}]')


class LexerError(CompilerError):

    def print_err(self):
        print(f'[LexERROR] [file={self.file}:line={self.line}:pos={self.pos}] [{self.msg}]')


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
        print(f'[ParseERROR] [file={self.file}:line={self.line}:pos={self.pos}] [{self.msg}] '
              f'[expected={self.exp_token}, found={self.curr_token}]')
