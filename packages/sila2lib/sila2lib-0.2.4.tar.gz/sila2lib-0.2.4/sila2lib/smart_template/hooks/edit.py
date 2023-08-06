"""
Module that pre-defines hooks that allow to actually edit the text of a template variable.
"""


def replace(input_string: str, old: str, new: str, count: int = None) -> str:
    """
    Replace elements in the input string.

        :param input_string: The input string in which the text is to be replaced.
        :param old: The old string element.
        :param new: The replacement text.
        :param count: How many times the text should be replaced. If None all occurrences will be replaced.
    """
    if count is None:
        return input_string.replace(old, new)
    else:
        return input_string.replace(old, new, count)
