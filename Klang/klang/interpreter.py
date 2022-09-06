""" Interpreter
The interpreter takes in an AST of nodes
Interprets it and return the desired result
"""

# pylint: disable = wildcard-import, unused-wildcard-import, invalid-name, unnecessary-lambda-assignment, unused-argument
from .constants import *
from .util import *
from .types import *
from .error import RTError


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

    def visit_StringNode(self, node, context):
        """ String Node """
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_ListNode(self, node, context):
        """ List Node """
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(
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

        value = value.copy().set_pos(node.pos_start,
                                     node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        """ Assign Variable """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.should_return():
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_VarReassignNode(self, node, context):
        """ Reassign Variable """
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.should_return():
            return res

        original_value = context.symbol_table.get(var_name)

        if original_value:
            context.symbol_table.set(var_name, value)
            return res.success(value)

        return res.failure(
            RTError(node.pos_start, node.pos_end, f"{var_name} is not defined",
                    context))

    def visit_BinOpNode(self, node, context):
        """ Binary Operation Node """
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))

        if res.should_return():
            return res

        right = res.register(self.visit(node.right_node, context))

        if res.should_return():
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)

        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)

        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)

        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)

        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)

        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)

        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)

        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)

        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)

        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)

        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)

        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)

        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        """ Unary Operation Node """
        res = RTResult()
        number = res.register(self.visit(node.node, context))

        if res.should_return():
            return res

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        elif node.op_tok.matches(TT_KEYWORD, "not"):
            number, error = number.notted()

        if error:
            return res.failure(error)

        return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        """ If statement """
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))

            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))

                if res.should_return():
                    return res

                return res.success(
                    Number.NULL if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res

            return res.success(
                Number.NULL if should_return_null else expr_value)

        return res.success(Number.NULL)

    def visit_ForNode(self, node, context):
        """ For Loop """
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node,
                                                 context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return(
            ) and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.NULL if node.should_return_null else List(elements).
            set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_WhileNode(self, node, context):
        """ While Loop """
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return(
            ) and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Number.NULL if node.should_return_null else List(elements).
            set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_FuncDefNode(self, node, context):
        """ Function """
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(
            func_name, body_node, arg_names,
            node.should_auto_return).set_context(context).set_pos(
                node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        """ Call Function """
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res

        value_to_call = value_to_call.copy().set_pos(node.pos_start,
                                                     node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res

        if return_value:
            return_value = return_value.copy().set_pos(
                node.pos_start, node.pos_end).set_context(context)

        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        """ Return """
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Number.NULL

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        """ Continue """
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        """ Break """
        return RTResult().success_break()
