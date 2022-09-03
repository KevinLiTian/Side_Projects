""" Parser
The parser takes in a list of tokens tokenized by the lexer
Processes them into an abstract syntax tree (AST) of nodes

Nodes are defined in "helper.py", some examples are
Number Node, If Node, For/While Loop Node, Function Node
"""
# pylint: disable = wildcard-import, unused-wildcard-import, line-too-long
from .constants import *
from .util import *
from .error import InvalidSyntaxError


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

    def peek_behind(self):
        """ Peek the previous Token """
        if self.tok_idx > 0:
            return self.tokens[self.tok_idx - 1]

        return None

    def peek_ahead(self):
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
            prev_token = self.peek_behind()
            next_tok = self.peek_ahead()

            if next_tok and next_tok.type == TT_EQ:
                if prev_token and prev_token.matches(TT_KEYWORD, "IF"):
                    res.register_advancement()
                    self.advance()
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_start.copy().advance(),
                            "Unexpected '=', maybe you meant '=='?"))

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
                    "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
                ))

        return res.success(node)

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

    def arith_expr(self):
        """ Fifth Prio """
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        """ Fourth Prio """
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

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

    def power(self):
        """ Second Prio """
        return self.bin_op(self.call, (TT_POW, ), self.factor)

    def call(self):
        """ Call """
        res = ParseResult()
        atom = res.register(self.atom())

        if res.error:
            return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()

            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
                        ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(
                        InvalidSyntaxError(self.current_tok.pos_start,
                                           self.current_tok.pos_end,
                                           "Expected ',' or  ')'"))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(node_to_call=atom,
                                        arg_nodes=arg_nodes))

        return res.success(atom)

    def atom(self):
        """ Highest Prio """
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        if tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

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

        if tok.matches(TT_KEYWORD, "FOR"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res

            return res.success(for_expr)

        if tok.matches(TT_KEYWORD, "WHILE"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res

            return res.success(while_expr)

        if tok.matches(TT_KEYWORD, "FUN"):
            func_def = res.register(self.func_def())
            if res.error:
                return res

            return res.success(func_def)

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start, tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', 'IF', 'FOR', 'WHILE', 'FUN'"
            ))

    def if_expr(self):
        """ If Statement """
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected 'IF'"))

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

    def for_expr(self):
        """ For Loop """
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected 'FOR'"))

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
                                   self.current_tok.pos_end, "Expected '='"))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected 'TO'"))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end,
                                   "Expected 'THEN'"))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(
            ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        """ While Loop"""
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end,
                                   "Expected 'WHILE'"))

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

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def func_def(self):
        """ Define Function """
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FUN"):
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected 'FUN'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected '('"))

        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected identifier or '('"))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(
                        InvalidSyntaxError(self.current_tok.pos_start,
                                           self.current_tok.pos_end,
                                           "Expected identifier"))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected ',' or ')'"))

        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start,
                                       self.current_tok.pos_end,
                                       "Expected identifier or ')'"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_ARROW:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start,
                                   self.current_tok.pos_end, "Expected '=>'"))

        res.register_advancement()
        self.advance()
        body_node = res.register(self.expr())

        if res.error:
            return res

        return res.success(
            FuncDefNode(var_name_tok=var_name_tok,
                        arg_name_toks=arg_name_toks,
                        body_node=body_node))

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