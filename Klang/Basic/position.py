""" Position """


class Position:
    """ Position of Text """

    def __init__(self, idx, line_number, col, file_name, file_text):
        self.idx = idx
        self.line_number = line_number
        self.col = col
        self.file_name = file_name
        self.file_text = file_text

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
