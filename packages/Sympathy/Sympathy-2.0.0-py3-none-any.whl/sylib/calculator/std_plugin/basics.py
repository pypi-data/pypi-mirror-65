# This file is part of Sympathy for Data.
# Copyright (c) 2013, Combine Control Systems AB
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
import inspect
import collections

import numpy as np


class LogicOperator(object):
    @staticmethod
    def nand(arr1, arr2):
        """
        Logical nand operator. Equivalent to np.logical_not(np.logical_and).
        """
        return np.logical_not(np.logical_and(arr1, arr2))

    @staticmethod
    def nor(arr1, arr2):
        """
        Logical nor operator. Equivalent to np.logical_not(np.logical_or).
        """
        return np.logical_not(np.logical_or(arr1, arr2))


class Statistics(object):
    @staticmethod
    def median(arr):
        """
        Median. Equivalent to np.ma.median except for the case where all values
        are masked. This function then returns NaN.
        """
        res = np.ma.median(arr)
        if res is np.ma.masked:
            res = np.float64('nan')
        return res


# TODO: docstrings and eval text should match better.
ARITHMETICS_OPS = [
    ("+ (plus)", "a + b", "Plus"),
    ("- (minus)", "a - b", "Minus"),
    ("* (times)", "a * b", "Multiplication"),
    ("** (power)", "a ** b", "Power."),
    ("/ (true division)", "a / b", "Division."),
    ("// (floor division)", "a // b", "floor division or integer division"),
    ("% (remainder)", "a % b", inspect.getdoc(np.mod)),
    ("divmod (floor division and remainder)", "divmod(a, b)",
     inspect.getdoc(divmod)),
]


# TODO: docstrings and eval text should match better.
COMPARATORS = [
    ("== (equal)", "a == b", inspect.getdoc(np.equal)),
    ("!= (not equal)", "a != b",
     inspect.getdoc(np.not_equal)),
    ("> (more than)", "a > b", inspect.getdoc(np.greater)),
    ("< (less than)", "a < b", inspect.getdoc(np.less)),
    (">= (more or equal)", "a >= b",
     inspect.getdoc(np.greater_equal)),
    ("<= (less or equal)", "a <= b",
     inspect.getdoc(np.less_equal)),
]


LOGIC_OPS = [
    ("not", "np.logical_not(a)",
     inspect.getdoc(np.logical_not)),
    ("and", "np.logical_and(a, b)",
     inspect.getdoc(np.logical_and)),
    ("or", "np.logical_or(a, b)",
     inspect.getdoc(np.logical_or)),
    ("all", "all(a)",
     inspect.getdoc(all)),
    ("any", "any(a)",
     inspect.getdoc(any)),
    ("xor", "np.logical_xor(a, b)",
     inspect.getdoc(np.logical_xor)),
    ("nand", "ca.nand(a, b)",
     inspect.getdoc(LogicOperator.nand)),
    ("nor", "ca.nor(a, b)",
     inspect.getdoc(LogicOperator.nor)),
]


# TODO: docstrings and eval text should match better.
BITWISE = [
    ("~ (not)", "~a", inspect.getdoc(np.bitwise_not)),
    ("& (and)", "a & b", inspect.getdoc(np.bitwise_and)),
    ("| (or)", "a | b", inspect.getdoc(np.bitwise_or)),
    ("^ (xor)", "a ^ b", inspect.getdoc(np.bitwise_xor)),
    ("<< (left shift)", "a << value", inspect.getdoc(np.left_shift)),
    (">> (right shift)", "a >> value",
     inspect.getdoc(np.right_shift)),
]


OPERATORS = collections.OrderedDict([
    ("Arithmetics", ARITHMETICS_OPS),
    ("Comparators", COMPARATORS),
    ("Logics", LOGIC_OPS),
    ("Bitwise", BITWISE),
])


STATISTICS = [
    ("Sum", "sum(a)", inspect.getdoc(sum)),
    ("Min", "min(a)", inspect.getdoc(min)),
    ("Max", "max(a)", inspect.getdoc(max)),
    ("Mean", "np.mean(a)", inspect.getdoc(np.mean)),
    ("Standard deviation", "np.std(a)", inspect.getdoc(np.std)),
    ("Median", "ca.median(a)", inspect.getdoc(np.ma.median)),
    ("Percentile", "np.percentile(a, value)",
     inspect.getdoc(np.percentile)),
]


GUI_DICT = collections.OrderedDict([
        ("Operators", OPERATORS),
        ("Statistics", STATISTICS),
    ])
