""" Utility Classes & Functions """


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
