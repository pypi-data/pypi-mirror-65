"""
Module that pre-defines a number of common hooks that influence the visual representation of the string.
"""


def lower(input_string: str) -> str:
    """Convert the complete string to lowercase."""
    return input_string.lower()


def upper(input_string: str) -> str:
    """Convert the complete string to uppercase."""
    return input_string.upper()


def capitalise(input_string: str) -> str:
    """Convert the first character of the string to uppercase."""
    return input_string[0].upper() + input_string[1:]
