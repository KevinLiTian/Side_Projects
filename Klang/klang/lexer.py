""" Lexer
The lexer takes text input (Klang Code)
Tokenizes it into a list of tokens

Tokens are defined in "constants.py", some examples are
math operators, keywords and logic operators
"""
# pylint: disable = wildcard-import, unused-wildcard-import
from .constants import *
from .util import Position
from .error import IllegalCharError, ExpectedCharError


class Lexer:
    """ Tokenize Input """

    def __init__(self, file_name, text):
        self.text = text
        self.file_name = file_name
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        """ Increment Pointer """
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        """ Create Tokens """
        tokens_list = []

        while self.current_char is not None:

            # Ignore Space or Tab
            if self.current_char in ' \t':
                self.advance()

            # Number
            elif self.current_char in DIGITS:
                tokens_list.append(self.make_number())

            # Identifier
            elif self.current_char in LETTERS:
                tokens_list.append(self.make_identifier())

            # String
            elif self.current_char == '"':
                token, error = self.make_string()
                if error:
                    return [], error
                tokens_list.append(token)

            # Math
            elif self.current_char == '+':
                tokens_list.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens_list.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens_list.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens_list.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens_list.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens_list.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens_list.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens_list.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()

            # Logics
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens_list.append(tok)

            elif self.current_char == '=':
                tokens_list.append(self.make_equals())

            elif self.current_char == '<':
                tokens_list.append(self.make_less_than())

            elif self.current_char == '>':
                tokens_list.append(self.make_greater_than())

            # No matching character
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos,
                                            "'" + char + "'")

        # Note end of file
        tokens_list.append(Token(TT_EOF, pos_start=self.pos))
        return tokens_list, None

    def make_string(self):
        """ Create String Token """
        string_literal = ""
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {'n': '\n', 't': '\t'}

        while self.current_char is not None and (self.current_char != '"'
                                                 or escape_character):
            if escape_character:
                string_literal += escape_characters.get(
                    self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string_literal += self.current_char

            self.advance()

        if self.current_char != '"':
            return None, ExpectedCharError(pos_start=pos_start,
                                           pos_end=self.pos,
                                           details="Closing '\"'")
        self.advance()
        return Token(TT_STRING,
                     value=string_literal,
                     pos_start=pos_start,
                     pos_end=self.pos), None

    def make_number(self):
        """ Create number tokens """
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)

        return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        """ Create Identifier Tokens """
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        """ Not Equal Logical Operator """
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' after '!'")

    def make_equals(self):
        """ Single = and Logical == """
        pos_start = self.pos.copy()
        self.advance()

        tok_type = TT_EQ

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE

        elif self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        """ < or <= """
        pos_start = self.pos.copy()
        self.advance()

        tok_type = TT_LT

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        """ > or >= """
        pos_start = self.pos.copy()
        self.advance()

        tok_type = TT_GT

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
