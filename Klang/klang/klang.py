""" Klang Runner """

from .util import SymbolTable, Context
from .types import BuiltInFunction, Number
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.NULL)
global_symbol_table.set("TRUE", Number.TRUE)
global_symbol_table.set("FALSE", Number.FALSE)
global_symbol_table.set("PI", Number.PI)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_func", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)


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
