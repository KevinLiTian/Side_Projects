""" Error """


# ========== Coloured Text =========== #
class TextColors:
    """ Text Colors  """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ========== Error Indication Text with Arrows =========== #
def string_with_arrows(text, pos_start, pos_end):
    """ Arrow points to error """
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0:
        idx_end = len(text)

    # Generate each line
    line_count = pos_end.line_number - pos_start.line_number + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

    return result.replace('\t', '')


class Error:
    """ Base Error Class """

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """ Print Out Error """
        result = f"\n{TextColors.FAIL}Klang {self.error_name}{TextColors.ENDC}: {self.details}\n"
        result += f"In file {self.pos_start.file_name}, on line {self.pos_start.line_number + 1}"
        result += '\n\n' + string_with_arrows(self.pos_start.file_text,
                                              self.pos_start, self.pos_end)

        return result


class IllegalCharError(Error):
    """ Illegal Character """

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    """ Expected Character """

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)


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
        result += f"{TextColors.FAIL}Klang {self.error_name}{TextColors.ENDC}: {self.details}"
        result += '\n\n' + string_with_arrows(self.pos_start.file_text,
                                              self.pos_start, self.pos_end)

        return result

    def generate_traceback(self):
        """ Generate Traceback Description """
        result = ''
        pos = self.pos_start
        context = self.context

        while context:
            description = f"In file {pos.file_name}, "
            description += f"on line {str(pos.line_number + 1)}, "
            description += f"in program {context.display_name}\n"
            result = description + result
            pos = context.parent_entry_pos
            context = context.parent

        return f"\n{TextColors.FAIL}Klang Error Traceback:{TextColors.ENDC}\n" + result
