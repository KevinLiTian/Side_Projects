""" Utility Classes & Functions """

# pylint: disable = import-outside-toplevel, arguments-differ, missing-function-docstring, unused-argument
from .error import RTError


# ========== Parser Result Register =========== #
class ParseResult:
    """ Result from Parser """

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def __repr__(self):
        return f"{self.node}"

    def register(self, res):
        """ Register Result """
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def register_advancement(self):
        """ Register an advancement result """
        self.advance_count += 1

    def success(self, node):
        """ Success """
        self.node = node
        return self

    def failure(self, error):
        """ Failure """
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


# ========== Runtime Result Register =========== #
class RTResult:
    """ Runtime Result """

    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        """ Register Runtime Result """
        if res.error:
            self.error = res.error

        return res.value

    def success(self, value):
        """ Success """
        self.value = value
        return self

    def failure(self, error):
        """ Failure """
        self.error = error
        return self


# ========== Token Position Indicator =========== #
class Position:
    """ Position of Text """

    def __init__(self, idx, line_number, col, file_name, file_text):
        self.idx = idx
        self.line_number = line_number
        self.col = col
        self.file_name = file_name
        self.file_text = file_text

    def __repr__(self):
        return f"File {self.file_name} line {self.line_number + 1} position {self.col}\n"

    def advance(self, current_char=None):
        """ Move to next char """
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line_number += 1
            self.col = 0

        return self

    def copy(self):
        """ Get a copy of current position """
        return Position(self.idx, self.line_number, self.col, self.file_name,
                        self.file_text)


# ========== Variable - Value Storage =========== #
class SymbolTable:
    """ Dictionary of Variables """

    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        """ Access a variable """
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)

        return value

    def set(self, name, value):
        """ Initialize a variable """
        self.symbols[name] = value

    def remove(self, name):
        """ Remove a variable """
        del self.symbols[name]


# ========== Runtime Traceback =========== #
class Context:
    """ Error Traceback """

    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


# ========== Value Types =========== #
class Base:
    """ Value Types Base Class """

    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        """ Set Position """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        """ Set Context """
        self.context = context
        return self

    # ========== To Be Overriden =========== #
    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RTError(self.pos_start, other.pos_end, 'Illegal operation',
                       self.context)


class Number(Base):
    """ Number Type """

    def __init__(self, value):
        super().__init__()
        self.value = value

    # ========== Override Math Operations =========== #
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end,
                                     'Division by zero', self.context)

            return Number(self.value / other.value).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(
                self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value
                              and other.value)).set_context(self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value
                              or other.value)).set_context(self.context), None
        else:
            return None, Base.illegal_operation(self, other)

    def notted(self):
        if self.value == 1 or self.value == 0:
            return Number(1 if self.value == 0 else 0).set_context(
                self.context), None

        return None, Base.illegal_operation(self, None)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)


Number.NULL = Number(0)
Number.FALSE = Number(0)
Number.TRUE = Number(1)


class String(Base):
    """ String Type """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f'"{self.value}"'

    def __str__(self):
        return self.value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(
                self.context), None

        return None, Base.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(
                self.context), None

        return None, Base.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy


class List(Base):
    """ List Type """

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy


class BaseFunction(Base):
    """ Function Base Type """

    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(
                RTError(
                    self.pos_start, self.pos_end,
                    f"{len(args) - len(arg_names)} too many args passed into {self}",
                    self.context))

        if len(args) < len(arg_names):
            return res.failure(
                RTError(
                    self.pos_start, self.pos_end,
                    f"{len(arg_names) - len(args)} too few args passed into {self}",
                    self.context))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i, value in enumerate(args):
            arg_name = arg_names[i]
            arg_value = value
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error:
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class Function(BaseFunction):
    """ Function Type """

    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        from .interpreter import Interpreter

        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(
            self.check_and_populate_args(self.arg_names, args, exec_ctx))

        if res.error:
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error:
            return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"


class BuiltInFunction(BaseFunction):
    """ Built-In Functions """

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        res.register(
            self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error:
            return res

        return_value = res.register(method(exec_ctx))
        if res.error:
            return res

        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    # ========= Built-In Functions =========== #

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(None)

    execute_print.arg_names = ['value']

    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = []

    def execute_clear(self, exec_ctx):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(None)

    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.TRUE if is_number else Number.FALSE)

    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.TRUE if is_number else Number.FALSE)

    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.TRUE if is_number else Number.FALSE)

    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"),
                               BaseFunction)
        return RTResult().success(Number.TRUE if is_number else Number.FALSE)

    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        list_.elements.append(value)
        return RTResult().success(list_)

    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        if not isinstance(index, Number):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Second argument must be number", exec_ctx))

        try:
            element = list_.elements.pop(index.value)
        except IndexError:
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end, 'Index is out of range',
                        exec_ctx))
        return RTResult().success(element)

    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        list1 = exec_ctx.symbol_table.get("listA")
        list2 = exec_ctx.symbol_table.get("listB")

        if not isinstance(list1, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        if not isinstance(list2, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Second argument must be list", exec_ctx))

        list1.elements.extend(list2.elements)
        return RTResult().success(None)

    execute_extend.arg_names = ["listA", "listB"]


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")


# ========== Parsed Nodes =========== #
class NumberNode:
    """ Number Type Node """

    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class StringNode:
    """ String Type Node """

    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class ListNode:
    """ List """

    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end


class VarAccessNode:
    """ Access Variable """

    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    """ Assign Variable """

    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarReassignNode:
    """ Reassign Variable """

    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class BinOpNode:
    """ Binary Operation """

    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode:
    """ Unary Operation """

    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


class IfNode:
    """ If statement """

    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0]
        self.pos_end = (self.else_case
                        or self.cases[len(self.cases) - 1][0]).pos_end


class ForNode:
    """ For Loop """

    def __init__(self, var_name_tok, start_value_node, end_value_node,
                 step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end


class WhileNode:
    """ While Loop """

    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end


class FuncDefNode:
    """ Function """

    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end


class CallNode:
    """ Function Call """

    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
