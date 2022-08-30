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

    def get_comparison_eq(self, other):
        """ Logical EQ """
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(
                self.context), None

    def get_comparison_ne(self, other):
        """ Logical NE """
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(
                self.context), None

    def get_comparison_lt(self, other):
        """ Logical LT """
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(
                self.context), None

    def get_comparison_gt(self, other):
        """ Logical GT """
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(
                self.context), None

    def get_comparison_lte(self, other):
        """ Logical LTE """
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(
                self.context), None

    def get_comparison_gte(self, other):
        """ Logical GTE """
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(
                self.context), None

    def anded_by(self, other):
        """ Logical AND """
        if isinstance(other, Number):
            return Number(int(self.value
                              and other.value)).set_context(self.context), None

    def ored_by(self, other):
        """ Logical OR """
        if isinstance(other, Number):
            return Number(int(self.value
                              or other.value)).set_context(self.context), None

    def notted(self):
        """ Logical NOT """
        return Number(1 if self.value == 0 else 0).set_context(
            self.context), None

    def copy(self):
        """ Get a copy of number """
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
