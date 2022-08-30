""" Interpreter """
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name

from .runtime import *
from .values import *
from .tokens import *


class Interpreter:
    """ Interpret AST """

    def visit(self, node, context):
        """ Run corresponding function depending on node type """
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        """ Exception """
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node, context):
        """ NumberNode """
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        """ Access Variable """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(node.pos_start, node.pos_end,
                        f"{var_name} is not defined", context))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        """ Assign Variable """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        """ Binary Operation Node """
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))

        if res.error:
            return res

        right = res.register(self.visit(node.right_node, context))

        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)

        elif node.op_tok.type == TT_MINUS:
            result, error = left.subtracted_by(right)

        elif node.op_tok.type == TT_MUL:
            result, error = left.multiplied_by(right)

        elif node.op_tok.type == TT_DIV:
            result, error = left.divided_by(right)

        elif node.op_tok.type == TT_POW:
            result, error = left.powered_by(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        """ Unary Operation Node """
        res = RTResult()
        number = res.register(self.visit(node.node, context))

        if res.error:
            return res

        if node.op_tok.type == TT_MINUS:
            number, error = number.multiplied_by(Number(-1))

        if error:
            return res.failure(error)

        return res.success(number.set_pos(node.pos_start, node.pos_end))
