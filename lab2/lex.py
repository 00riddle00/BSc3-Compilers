from sys import argv

from lexer import Input, Lexer

file_to_lex = 'tmp.fx'
if len(argv) == 2:
    file_to_lex = argv[1]

with open(file_to_lex) as f:
    content = ''.join(f.readlines())

    try:
        _input = Input(file_to_lex, content)
        lexer = Lexer(_input)
        lexer.lex_all()
        lexer.dump_tokens()
    except ValueError:
        pass
