""" Error """
from .util import string_with_arrows


class Error:
    """ Base Error Class """

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """ Print Out Error """
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.file_name}, line {self.pos_start.line_number + 1}"
        result += '\n\n' + string_with_arrows(self.pos_start.file_text,
                                              self.pos_start, self.pos_end)

        return result


class IllegalCharError(Error):
    """ Illegal Character """

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    """ Illegal Syntax in Parsing"""

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Syntax', details)


class RTError(Error):
    """ Runtime Error """

    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        """ Print Out Error """
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += '\n\n' + string_with_arrows(self.pos_start.file_text,
                                              self.pos_start, self.pos_end)

        return result

    def generate_traceback(self):
        """ Generate Traceback Description """
        result = ''
        pos = self.pos_start
        context = self.context

        while context:
            description = f"  File {pos.file_name}, "
            description += f"line {str(pos.line_number + 1)}, in {context.display_name}\n"
            result = description + result
            pos = context.parent_entry_pos
            context = context.parent

        return "\nTraceback (most recent call last):\n" + result