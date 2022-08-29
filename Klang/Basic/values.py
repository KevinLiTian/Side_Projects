""" Values """
# pylint: disable=unused-wildcard-import,wildcard-import

from .error import *


class Number:
    """ Number Type """

    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def __repr__(self):
        return str(self.value)

    def set_pos(self, pos_start=None, pos_end=None):
        """ Set Position """
        self.pos_start = pos_start
        self.pos_end = pos_end

        return self

    def set_context(self, context=None):
        """ Set Trackback """
        self.context = context
        return self

    def added_to(self, other):
        """ Add Method """
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None

    def subtracted_by(self, other):
        """ Subtract Method """
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None

    def multiplied_by(self, other):
        """ Multiply Method """
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None

    def divided_by(self, other):
        """ Divide Method """
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end,
                                     "Division by zero", self.context)
            return Number(self.value / other.value).set_context(
                self.context), None

    def powered_by(self, other):
        """ Power Method """
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(
                self.context), None
