from sys import argv

from lexer import Input, Lexer

file_to_lex = 'tmp.fx'
if len(argv) == 2:
    file_to_lex = argv[1]

try:
    _input = Input(file_to_lex)
    lexer = Lexer([_input])
    lexer.lex_all()
    lexer.dump_tokens()
except ValueError:
    print('exception while starting Lexer')
