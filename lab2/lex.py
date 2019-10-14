from sys import argv

from lexer import Lexer

file_to_lex = 'tmp.fx'
if len(argv) == 2:
    file_to_lex = argv[1]

import pprint

with open(file_to_lex) as f:
    content = ''.join(f.readlines())

    print(10*'#')
    pprint.pprint(content)
    print(10*'#')

    try:
        lexer = Lexer(content)
        lexer.lex_all()
        lexer.dump_tokens()
    except ValueError:
        pass
