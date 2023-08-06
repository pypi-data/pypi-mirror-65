"""
Module that defines custom exceptions used in this package
"""


class KeyExistsError(LookupError):
    """Raise when the key in the dictionary already exists."""


class TypeWarning(Warning):
    """Raised equivalent the a TypeError, but not fatal for the execution."""
