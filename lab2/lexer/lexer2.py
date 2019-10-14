
    def lex_all(self):
        while self.running and self.offset < len(self._input):
            self.curr_char = self._input[self.offset]
            # if self.curr_char == '\n':
            #     self.line_no += 1; # BAAAAD!!!!
            self.lex_char()
            self.offset += 1

        if self.running:
            self.curr_char = '\n'
            self.lex_char()
            if self.state != ':START':
                self.lexer_error(f'unterminated something {self.state}', None)

    def lex_char(self):
        if self.state == ':COMMENT':
            self.lex_comment()
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
            raise Exception(f'invalid state')

    def lex_comment(self):
        if self.curr_char == '\n':
            self.line_no += 1
            self.state = ':START'
        else:
            pass  # ignore

    def lex_start(self):
        if self.curr_char == '#':
            self.state = ':COMMENT'





