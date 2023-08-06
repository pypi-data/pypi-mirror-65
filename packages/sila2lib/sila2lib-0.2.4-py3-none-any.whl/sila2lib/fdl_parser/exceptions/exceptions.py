"""
Module that defines custom exceptions and warnings used in this package
"""


class KeyExistsError(LookupError):
    """Raise when the key in the dictionary already exists."""


class SubDataTypeError(TypeError):
    """Raise when a sub-type of a :class:`~..FDLParser.DataType` is invalid."""


class TypeWarning(Warning):
    """
    General warning for invalid types.
        Analogue to the TypeError, just allows to continue the process.
    """


class DataTypeWarning(TypeWarning):
    """General warning for an invalid DataType."""


class BasicTypeWarning(DataTypeWarning):
    """Expected a :class:`~..FDLParser.BasicType` object."""


class SubDataTypeWarning(DataTypeWarning):
    """An unexpected sub-type of a :class:`~..FDLParser.DataType` element has been found."""


class ConstraintTypeWarning(DataTypeWarning):
    """A constraint found does not work with the given :class:`~..FDLParser.DataType` element."""


class ConstraintValueWarning(DataTypeWarning):
    """The value for a given constraint is outside of the valid range."""


class ConstraintUnsupportedContentType(DataTypeWarning):
    """The given content type is not officially supported."""
