""" Lexer """
# pylint: disable=unused-wildcard-import,wildcard-import

from .constants import *
from .position import *
from .tokens import *
from .error import *


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
            elif self.current_char in DIGITS:
                tokens_list.append(self.make_number())
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
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos,
                                            "'" + char + "'")

        tokens_list.append(Token(TT_EOF, pos_start=self.pos))
        return tokens_list, None

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
