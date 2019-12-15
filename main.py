from sys import argv

from lexer import Input, Lexer
from parser import Parser, ASTPrinter, Scope
from errors import LexerError, ParserError, InputError, SemanticError, InternalError

samples_dir = 'FXlang_samples'

file_to_lex = f'{samples_dir}/tmp.fx'
if len(argv) == 2:
    file_to_lex = f'{samples_dir}/{argv[1]}'

try:
    _input = Input(file_to_lex)
    lexer = Lexer([_input])
    lexer.lex_all()
    lexer.dump_tokens()
    parser = Parser(_input, lexer.tokens)
    root = parser.parse_program()
    printer = ASTPrinter()
    printer.print('root', root)

    root_scope = Scope()
    root.resolve_names(root_scope)
    root.check_types()
# todo wrap in CompilerError
except InputError as ie:
    ie.print_err()
except LexerError as le:
    le.print_err()
except ParserError as pe:
    pe.print_err()
except SemanticError as se:
    se.print_err()
except InternalError as ie:
    ie.print_err()
