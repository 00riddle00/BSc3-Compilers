from sys import argv

from lexer import Input, Lexer
from parser import Parser, ASTPrinter

samples_dir = 'FXlang_samples'

file_to_lex = f'{samples_dir}/tmp.fx'
if len(argv) == 2:
    file_to_lex = f'{samples_dir}/{argv[1]}'

try:
    _input = Input(file_to_lex)
    lexer = Lexer([_input])
    lexer.lex_all()
    lexer.dump_tokens()
except ValueError:
    print('exception while starting Lexer')

try:
    parser = Parser(lexer.tokens)
    # root = parser.parse_expr()
    root = parser.parse_decl_fn()
    printer = ASTPrinter()
    printer.print('root', root)
except ValueError:
    print('exception while starting Parser')



