from sys import argv

from lexer import Input, Lexer
from parser import Parser, ASTPrinter
from errors import LexerError, ParserError, InputError

samples_dir = 'FXlang_samples'

file_to_lex = f'{samples_dir}/tmp.fx'
if len(argv) == 2:
    file_to_lex = f'{samples_dir}/{argv[1]}'

try:
    _input = Input(file_to_lex)
except InputError as ie:
    ie.print_err()
    exit(1)

try:
    lexer = Lexer([_input])
    lexer.lex_all()
    lexer.dump_tokens()
except LexerError as le:
    le.print_err()

try:
    parser = Parser(_input, lexer.tokens)
    root = parser.parse_program()
    printer = ASTPrinter()
    printer.print('root', root)
except ParserError as pe:
    pe.print_err()
