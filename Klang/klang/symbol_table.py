""" Store Variables """


class SymbolTable:
    """ Dictionary of Variables """

    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        """ Access a variable """
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)

        return value

    def set(self, name, value):
        """ Initialize a variable """
        self.symbols[name] = value

    def remove(self, name):
        """ Remove a variable """
        del self.symbols[name]
