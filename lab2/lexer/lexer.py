
class Lexer:
    tokens: list
    text: str
    offset: int

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
