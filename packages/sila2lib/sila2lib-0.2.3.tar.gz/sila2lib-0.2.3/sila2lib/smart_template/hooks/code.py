"""
Module that pre-defines a number of common hooks that can be used for code formatting.
"""

# import general packages
import re
import textwrap


def indent(input_string: str, indentation: int) -> str:
    r"""
    Indent the given string.

        :param input_string: The string to indent. If the string spans several lines, every line will be indented
                             (assumed separator \\n).
        :param indentation: Number of spaces used to indent every line of the input string.

    """

    return (
        " " * indentation +
        input_string.replace('\n', "\n" + " " * indentation)
    )


def trim(input_string: str, left: bool = True, right: bool = True) -> str:
    r"""
    Trim whitespace around the string.
        This function removes whitespace from a string. If the string spans multiple lines, the whitespace will be
        removed from every line.

        :param input_string: The string which should be trimmed.
        :param left: Trim whitespace on the left side of the string.
        :param right: Trim whitespace on the right side of the string.

        :return: The trimmed string.
    """

    # To achieve multi-line replacement without a loop, use regular expressions
    pattern_search = r'^(?P<left>\s*)(?P<text>.*?)(?P<right>\s*)$'

    # define the replacement pattern based on the whitespace to be removed
    if left and right:
        pattern_replace = r'\g<text>'
    elif left:
        pattern_replace = r'\g<text>\g<right>'
    elif right:
        pattern_replace = r'\g<left>\g<text>'
    else:
        return input_string

    return re.sub(pattern_search, pattern_replace, input_string, flags=re.MULTILINE)


def wrap(input_string: str, width: int = 120) -> str:
    r"""
    Wraps a text to a maximum width.
    
    :param input_string: The string which should be wrapped.
    :param width: The maximum width allowed for a line in the text.
    
    :return: The input string with wrapped lines.
    """
    return "\n".join([
        textwrap.fill(item, width) for item in input_string.splitlines()
    ])
