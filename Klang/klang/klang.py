""" Klang Runner """

from .util import SymbolTable, Number, Context
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("TRUE", Number(1))
global_symbol_table.set("FALSE", Number(0))


def run(file_name, text):
    """ Higer Level Run Function """

    # Generate Tokens
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error

    # Generate Abstract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
