""" Constants """

# ========== Constants =========== #
import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

# ========== Keyword Constants =========== #
KEYWORDS = [
    "let", "and", "or", "not", "if", "then", "elif", "else", "for", "to",
    "step", "while", "fun", "end", "return", "continue", "break", "do"
]

# ========== Token Type (TT) Constants =========== #
# Math
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

# Variable
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EQ = "EQ"

# Logics
TT_EE = "EE"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"

# Function
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"

# String
TT_STRING = "STRING"

# List
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"

# Other
TT_NEWLINE = "NEWLINE"
TT_EOF = "EOF"


class Token:
    """ Tokens """

    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"

        return f"{self.type}"

    def matches(self, type_, value=None):
        """ Check for Token Equality """
        return self.type == type_ and self.value == value
