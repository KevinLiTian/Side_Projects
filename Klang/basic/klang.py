""" Klang Basics """

from .lexer import Lexer
from .parse import Parser
from .interpreter import Interpreter
from .context import Context


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
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
