
keywords = {
  'if': 'KW_IF',
  'return': 'KW_RETURN',
  'while': 'KW_WHILE',
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
    tokens: list = ["2", "+", "3"]
    text: str = "2+3"
    offset: int = 4

    def __init__(self, text: str) -> None:
        assert len(text)

    def lex_all(self):
        try:
            while self.offset < len(self.text):
                pass

        except BufferError as e:
            print(str(e))
            raise ValueError()

        return self.tokens

    def lex(self):
        pass

    def print_tokens(self):
        pass









