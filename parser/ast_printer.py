from lexer import Token
from .ast import Node


class ASTPrinter:

    def __init__(self):
        self.indent_level = 0

    def print(self, title, obj):
        if isinstance(obj, Node):
            self.print_node(title, obj)
        elif isinstance(obj, list):
            self.print_array(title, obj)
        elif isinstance(obj, Token):
            self.print_token(title, obj)
        elif not obj:
            self.print_single(title, 'NULL')
        else:
            print(f'bad argument {obj.__class__.__name__}')
            exit(1)

    def print_array(self, title, array):
        if not array:
            self.print_single(title, '[]')

        for ind, el in enumerate(array):
            self.print(f'{title}[{ind}]', el)

    def print_node(self, title, node):
        self.print_single(title, f'{node.__class__.__name__}:')
        self.indent_level += 1
        node.print_node(self)
        self.indent_level -= 1

    def print_single(self, title, text):
        prefix = '  ' * self.indent_level
        print(f'{prefix}{title}: {text}')

    def print_token(self, title, token):
        if token.value == '':
            text = f'{token.type} (ln={token.line_no})'
        else:
            text = f'{token.value} (ln={token.line_no})'
        self.print_single(title, text)
