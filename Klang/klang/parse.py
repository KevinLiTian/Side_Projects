""" Parse """
# pylint: disable=unused-wildcard-import,wildcard-import,too-many-function-args,line-too-long

from .tokens import *
from .nodes import *
from .error import *


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


class Parser:
    """ Parsing Tokens into Syntax Tree """

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        """Go to the Next Token """
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

        return self.current_tok

    def peek(self):
        """ Peek the Next Token """
        if self.tok_idx < len(self.tokens) - 1:
            return self.tokens[self.tok_idx + 1]

        return None

    def parse(self):
        """ High Level Parse Function """
        res = self.expr()

        # Not reaching end of file token after parsing, syntax error
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'AND' or 'OR'"
                ))
        return res

    def if_expr(self):
        """ If Statement """
        res = ParseResult()
        cases = []
        else_case = None

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())

        if res.error:
            return res

        if self.current_tok.type == TT_EQ:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_start.copy().advance(),
                                   "Unexpected '=', maybe you meant '=='?"))

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end,
                                   "Expected 'THEN'"))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())

        if res.error:
            return res

        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected 'THEN'"))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())

            if res.error:
                return res

            cases.append((condition, expr))

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())

            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def atom(self):
        """ Highest Prio """
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        if tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        if tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())

            if res.error:
                return res

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)

            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected ')'"))

        if tok.matches(TT_KEYWORD, "IF"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res

            return res.success(if_expr)

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start, tok.pos_end,
                "Expected int, float, identifier, '+', '-' or '('"))

    def power(self):
        """ Second Prio """
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        """ Third Prio """
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())

            if res.error:
                return res

            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        """ Fourth Prio """
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def arith_expr(self):
        """ Fifth Prio """
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def comp_expr(self):
        """ Sixth Prio """
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "NOT"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())

            if res.error:
                return res

            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(
            self.bin_op(self.arith_expr,
                        (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected int, float, identifier, '+', '-', '(' or NOT"))

        return res.success(node)

    def expr(self):
        """ General Priority  """
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected identifier"))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected '='"))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())

            if res.error:
                return res

            return res.success(VarAssignNode(var_name, expr))

        if self.current_tok.type == TT_IDENTIFIER:
            next_tok = self.peek()

            if next_tok and next_tok.type == TT_EQ:
                var_name = self.current_tok
                res.register_advancement()
                self.advance()
                res.register_advancement()
                self.advance()

                expr = res.register(self.expr())

                if res.error:
                    return res

                return res.success(VarReassignNode(var_name, expr))

        node = res.register(
            self.bin_op(self.comp_expr,
                        ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"))))

        if res.error:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'VAR', int, float, identifier, '+', '-' or '('"))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        """ Binary Operations """
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())

        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type,
                                               self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())

            if res.error:
                return res

            left = BinOpNode(left, op_tok, right)

        return res.success(left)
