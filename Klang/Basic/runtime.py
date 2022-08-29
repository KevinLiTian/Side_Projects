""" Runtime """


class RTResult:
    """ Runtime Result """

    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        """ Register Runtime Result """
        if res.error:
            self.error = res.error

        return res.value

    def success(self, value):
        """ Success """
        self.value = value
        return self

    def failure(self, error):
        """ Failure """
        self.error = error
        return self
