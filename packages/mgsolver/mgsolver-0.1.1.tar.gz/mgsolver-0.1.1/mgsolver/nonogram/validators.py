"""Validator are functions to validate input values.

Validators should not return anything rather raise an exception
if the inputs do not meet expected conditions.
"""

from src.messages import INT_GT_0


def int_gt_0(value: int):
    """Integer value greater than zero."""
    if type(value) is not int or value < 1:
        raise ValueError(INT_GT_0)


def ints_gt_0(*values):
    """Integers greater than zero."""
    for value in values:
        int_gt_0(value)
