"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Module for constrained data types.

:file:    type_constrained.py
:authors: Timm Severin

:date: (creation)          20190820
:date: (last modification) 20190820

__________________________________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
__________________________________________________________________________________________________
"""

# since we need to distinguish all the constraints, let us allow complex branches and a lot of return statements as well
#   as all these instance attributes
# pylint: disable=too-many-return-statements, too-many-branches, too-many-instance-attributes, too-many-statements

# import general packages used here
import warnings

# import meta packages
from typing import Any, List
from typing import Union, Optional

# import custom exceptions
from .exceptions.exceptions import SubDataTypeError, BasicTypeWarning, ConstraintTypeWarning, ConstraintValueWarning

# import library packages
from .type_base import DataType

from . import type_basic as b_type
from . import type_list as l_type

from .constraint_content_type import ConstraintContentType
from .constraint_schema import ConstraintSchema
from .constraint_unit import ConstraintUnit


class ConstrainedType(DataType):
    """
    Class for the derived SiLA data type that implements constraints.
    """

    #: The length constraint
    constraint_length: Optional[int]

    #: The minimal length constraint
    constraint_length_minimal: Optional[int]

    #: The maximal allowed length
    constraint_length_maximal: Optional[int]

    #: The element must be part of an enumeration
    constraint_set: Optional[List[Union[str, int, float]]]

    #: The element is constrained by a RegExp pattern
    constraint_pattern: Optional[str]

    #: The constraint for a maximal (exclusive) value
    constraint_value_maximal_exclusive: Optional[str]

    #: The constraint for a maximal (inclusive) value
    constraint_value_maximal_inclusive: Optional[str]

    #: The constraint for a minimal (exclusive) value
    constraint_value_minimal_exclusive: Optional[str]

    #: The constraint for a minimal (inclusive) value
    constraint_value_minimal_inclusive: Optional[str]

    #: A unit constraint
    constraint_unit: Optional[ConstraintUnit]

    #: Content type constraint
    constraint_content_type: Optional[ConstraintContentType]

    #: Constraint to require a fully qualified identifier
    constraint_identifier: Optional[str]

    #: Constrain the content to follow a schema
    constraint_schema: Optional[ConstraintSchema]

    # Constraints that are only applicable to lists
    #: Constraint for the exact number of elements in a list
    constraint_elements_count: Optional[int]

    #: Constraint for the minimal number of elements in a list
    constraint_elements_minimal: Optional[int]

    #: Constraint for the maximal number of elements in a list
    constraint_elements_maximal: Optional[int]

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <List>-xml element that contains this list type.

        :raises SubDataTypeError: Invalid sub-type found when trying to create the underlying DataType object.
        :raises SubDataTypeWarning: A warning that a sub-type is invalid, however the program can somehow continue.
                                    Some special case handling might however fail.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_constrained = True

        # Initialise constraints as undefined
        #   Basic types
        self.constraint_length = None
        self.constraint_length_minimal = None
        self.constraint_length_maximal = None
        self.constraint_set = None
        self.constraint_pattern = None
        self.constraint_value_maximal_exclusive = None
        self.constraint_value_maximal_inclusive = None
        self.constraint_value_minimal_exclusive = None
        self.constraint_value_minimal_inclusive = None
        self.constraint_unit = None
        self.constraint_content_type = None
        self.constraint_identifier = None
        self.constraint_schema = None
        # List types
        self.constraint_elements_count = None
        self.constraint_elements_minimal = None
        self.constraint_elements_maximal = None

        # Every constrained **must** have a DataType sub-element, so we create a sub-element from that
        if hasattr(xml_tree_element.DataType, 'Basic'):
            self.sub_type = b_type.BasicType(
                xml_tree_element=xml_tree_element.DataType.Basic
            )
        elif hasattr(xml_tree_element.DataType, 'List'):
            self.sub_type = l_type.ListType(
                xml_tree_element=xml_tree_element.DataType.List
            )
        elif hasattr(xml_tree_element.DataType, 'DataTypeIdentifier'):
            # I'm not sure if this is possible? Anyway, we cannot check whether the sub-type can be used for constraints
            #   without having access to the DataType storage in the main FDLParser.
            #   For now we assume that this is not allowed
            raise SubDataTypeError(
                'The type underlying a constraint data type is a DataTypeIdentifier. '
                'This is not allowed. '
                'Consider moving the constraint into the DataTypeDefinition of the corresponding identifier. '
            )
        else:
            # invalid type
            raise SubDataTypeError('Only SiLA Basic Types and Lists can be constrained.')

        # Let us try to find out the basic, underlying type. This expects the sub-type to be either a basic element, or
        #   a list of Basic elements. If this is not the case, we do not really know how to handle it.
        if isinstance(self.sub_type, b_type.BasicType):
            # Assume: Basic / org.silastandard.<type>
            type_underlying = self.sub_type.sub_type
        elif isinstance(self.sub_type, l_type.ListType):
            # Assume: List / Basic / org.silastandard.<type>
            type_underlying = self.sub_type.sub_type.sub_type
        else:
            warnings.warn('Invalid sub-type of the constrained type found. So far I am quite unaware of how to handle '
                          'the constraints.', BasicTypeWarning)
            type_underlying = None

        # if underlying type found is not a string we haven't found the basic type yet. However, if it is a list we can
        #   handle it for the element count constraints, so allow that. Everything else just warn, go on and hope for
        #   the best.
        if not isinstance(type_underlying, str) and not isinstance(self.sub_type, l_type.ListType):
            warnings.warn('Could not determine basic, underlying data type. So far I am quite unaware of how to handle '
                          'the constraints.', BasicTypeWarning)
            type_underlying = None

        # we read the constraints after the sub-type has been read, so we can validate whether it is possible to apply
        #   the given constraints to the underlying data-type
        if hasattr(xml_tree_element.Constraints, 'Length'):
            types_allowed = ["String", "Binary"]
            if type_underlying in types_allowed:
                self.constraint_length = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.Length,
                    constraint_name='Length'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='Length',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MinimalLength'):
            types_allowed = ["String", "Binary"]
            if type_underlying in types_allowed:
                self.constraint_length_minimal = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.MinimalLength,
                    constraint_name='MinimalLength'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MinimalLength',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MaximalLength'):
            types_allowed = ["String", "Binary"]
            if type_underlying in types_allowed:
                self.constraint_length_maximal = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.MaximalLength,
                    constraint_name='MaximalLength'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MaximalLength',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'Set'):
            types_allowed = ["String", "Integer", "Real", "Date", "Time", "Timestamp"]
            if type_underlying in types_allowed:
                self.constraint_set = []
                for set_value in xml_tree_element.Constraints.Set.Value:
                    self.constraint_set.append(set_value)
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='Set',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'Pattern'):
            types_allowed = ["String"]
            if type_underlying in types_allowed:
                self.constraint_pattern = xml_tree_element.Constraints.Pattern.text
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='Pattern',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MaximalExclusive'):
            types_allowed = ["Integer", "Real", "Date", "Time", "Timestamp"]
            if type_underlying in types_allowed:
                self.constraint_value_maximal_exclusive = xml_tree_element.Constraints.MaximalExclusive.text
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MaximalExclusive',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MaximalInclusive'):
            types_allowed = ["Integer", "Real", "Date", "Time", "Timestamp"]
            if type_underlying in types_allowed:
                self.constraint_value_maximal_inclusive = xml_tree_element.Constraints.MaximalInclusive.text
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MaximalInclusive',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MinimalExclusive'):
            types_allowed = ["Integer", "Real", "Date", "Time", "Timestamp"]
            if type_underlying in types_allowed:
                self.constraint_value_minimal_exclusive = xml_tree_element.Constraints.MinimalExclusive.text
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MinimalExclusive',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'MinimalInclusive'):
            types_allowed = ["Integer", "Real", "Date", "Time", "Timestamp"]
            if type_underlying in types_allowed:
                self.constraint_value_minimal_inclusive = xml_tree_element.Constraints.MinimalInclusive.text
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MinimalInclusive',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'Unit'):
            types_allowed = ["Integer", "Real"]
            if type_underlying in types_allowed:
                self.constraint_unit = ConstraintUnit(xml_tree_element=xml_tree_element.Constraints.Unit)
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='Unit',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'ContentType'):
            types_allowed = ["String", "Binary"]
            if type_underlying in types_allowed:
                self.constraint_content_type = ConstraintContentType(
                    xml_tree_element=xml_tree_element.Constraints.ContentType
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='ContentType',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'FullyQualifiedIdentifier'):
            types_allowed = ["String"]
            if type_underlying in types_allowed:
                identifiers_allowed = [
                    'FeatureIdentifier',
                    'CommandIdentifier',
                    'CommandParameterIdentifier',
                    'CommandResponseIdentifier',
                    'IntermediateCommandResponseIdentifier',
                    'DefinedExecutionErrorIdentifier',
                    'PropertyIdentifier',
                    'DataTypeIdentifier',
                    'MetaDataIdentifier'
                ]
                if xml_tree_element.Constraints.FullyQualifiedIdentifier.text in identifiers_allowed:
                    self.constraint_identifier = xml_tree_element.Constraints.FullyQualifiedIdentifier.text
                else:
                    warnings.warn(
                        (
                            'FullyQualifiedIdentifier constraint uses an invalid identifier: {identifier}. '
                            'This constraint will be ignored. '
                        ).format(
                            identifier=xml_tree_element.Constraints.FullyQualifiedIdentifier.text
                        ),
                        ConstraintValueWarning
                    )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='FullyQualifiedIdentifier',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        if hasattr(xml_tree_element.Constraints, 'Schema'):
            types_allowed = ["String", "Binary"]
            if type_underlying in types_allowed:
                self.constraint_schema = ConstrainedType._read_constraint_schema(
                    xml_constraint=xml_tree_element.Constraints.Schema
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='Schema',
                    type_allowed=types_allowed,
                    type_found=str(type_underlying)
                )

        # Special list constraints
        if hasattr(xml_tree_element.Constraints, 'ElementCount'):
            if isinstance(self.sub_type, l_type.ListType):
                self.constraint_elements_count = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.ElementCount,
                    constraint_name='ElementCount'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='ElementCount',
                    type_allowed=['List'],
                    type_found=str(self.sub_type)
                )

        if hasattr(xml_tree_element.Constraints, 'MinimalElementCount'):
            if isinstance(self.sub_type, l_type.ListType):
                self.constraint_elements_minimal = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.MinimalElementCount,
                    constraint_name='MinimalElementCount'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MinimalElementCount',
                    type_allowed=['List'],
                    type_found=str(self.sub_type)
                )

        if hasattr(xml_tree_element.Constraints, 'MaximalElementCount'):
            if isinstance(self.sub_type, l_type.ListType):
                self.constraint_elements_maximal = ConstrainedType._read_constraint_positive_integer(
                    xml_constraint=xml_tree_element.Constraints.MaximalElementCount,
                    constraint_name='MaximalElementCount'
                )
            else:
                ConstrainedType._constraint_type_warning(
                    constraint_name='MaximalElementCount',
                    type_allowed=['List'],
                    type_found=str(self.sub_type)
                )

    def __getitem__(self, key: str) -> Any:
        """
        Make the constraints available using a key (dictionary-like) call.

        :param key: The constraint property to read.

        :raises TypeError: Given `key` is not a valid string identifier.
        :raises KeyError: The given key is unknown.
        """

        # check the input type
        if not isinstance(key, str):
            raise TypeError

        if key == 'Length':
            return self.constraint_length
        elif key == 'MinimalLength':
            return self.constraint_length_minimal
        elif key == 'MaximalLength':
            return self.constraint_length_maximal
        elif key == 'Set':
            return self.constraint_set
        elif key == 'Pattern':
            return self.constraint_pattern
        elif key == 'MaximalExclusive':
            return self.constraint_value_maximal_exclusive
        elif key == 'MaximalInclusive':
            return self.constraint_value_maximal_inclusive
        elif key == 'MinimalExclusive':
            return self.constraint_value_minimal_exclusive
        elif key == 'MinimalInclusive':
            return self.constraint_value_minimal_inclusive
        elif key == 'Unit':
            return self.constraint_unit
        elif key == 'ContentType':
            return self.constraint_content_type
        elif key == 'FullyQualifiedIdentifier':
            return self.constraint_identifier
        elif key == 'Schema':
            return self.constraint_schema
        elif key == 'ElementCount':
            return self.constraint_elements_count
        elif key == 'MinimalElementCount':
            return self.constraint_elements_minimal
        elif key == 'MaximalElementCount':
            return self.constraint_elements_maximal
        else:
            raise KeyError

    def __setitem__(self, key: str, value: Any):
        """
        Make the constraints available using a key (dictionary-like) assignment operation.

        :param key: The constraint property to read.
        :param value: The value to set. This **will** automatically be converted to the required data type if necessary
                      (e.g. int or str). If this is not supported by the value given, an error might occur!

        :raises TypeError: Given `item` is not a valid string identifier.
        :raises KeyError: The given key is unknown.

        .. note:: This function does (unfortunately) **not** check whether the input is actually allowed. So you can set
                  arbitrary data, that does not conform to the SiLA standard. Please refrain from doing so, it might
                  break things that are not yours to break!
        """

        # check the input type
        if not isinstance(key, str):
            raise TypeError

        # store the input and explicitly convert it to the required data type.
        if key == 'Length':
            self.constraint_length = int(value)
        elif key == 'MinimalLength':
            self.constraint_length_minimal = int(value)
        elif key == 'MaximalLength':
            self.constraint_length_maximal = int(value)
        elif key == 'Set':
            self.constraint_set = [str(item) for item in value]
        elif key == 'Pattern':
            self.constraint_pattern = str(value)
        elif key == 'MaximalExclusive':
            self.constraint_value_maximal_exclusive = str(value)
        elif key == 'MaximalInclusive':
            self.constraint_value_maximal_inclusive = str(value)
        elif key == 'MinimalExclusive':
            self.constraint_value_minimal_exclusive = str(value)
        elif key == 'MinimalInclusive':
            self.constraint_value_minimal_inclusive = str(value)
        elif key == 'Unit':
            self.constraint_unit = value
        elif key == 'ContentType':
            self.constraint_content_type = value
        elif key == 'FullyQualifiedIdentifier':
            self.constraint_identifier = str(value)
        elif key == 'ElementCount':
            self.constraint_elements_count = int(value)
        elif key == 'MinimalElementCount':
            self.constraint_elements_minimal = int(value)
        elif key == 'MaximalElementCount':
            self.constraint_elements_maximal = int(value)
        else:
            raise KeyError

    @staticmethod
    def _read_constraint_positive_integer(xml_constraint, constraint_name: str) -> Optional[int]:
        """Method to read and validate a positive integer value from a constraint."""
        try:
            value = int(xml_constraint.text)
            if value > 0:
                return value
        except ValueError:
            pass

        ConstrainedType._constraint_value_warning(
            constraint_name=constraint_name,
            value_allowed=['Positive Integer'],
            value_found=xml_constraint.text
        )
        return None

    @staticmethod
    def _read_constraint_schema(xml_constraint) -> Optional[ConstraintSchema]:
        try:
            return ConstraintSchema(xml_tree_element=xml_constraint)
        except KeyError:
            ConstrainedType._constraint_value_warning(
                constraint_name='Schema.Type',
                value_allowed=['Xml', 'Json'],
                value_found=xml_constraint.Type.text
            )
        except TypeError:
            ConstrainedType._constraint_value_warning(
                constraint_name= 'Schema: <data>',
                value_allowed=['As <Url />', 'As <Inline />'],
                value_found='None of the above'
            )

        return None

    @staticmethod
    def _constraint_type_warning(constraint_name: str, type_allowed: List[str], type_found: str):
        warnings.warn(
            (
                'Constraint of type {constraint_name} can only be applied to the following data types: '
                '"{types_allowed}". Type found: {type_underlying}. '
                'Constrained will *not* be stored.'
            ).format(
                constraint_name=constraint_name,
                types_allowed=", ".join(type_allowed),
                type_underlying=str(type_found)
            ),
            ConstraintTypeWarning
        )

    @staticmethod
    def _constraint_value_warning(constraint_name: str, value_allowed: List[str], value_found: str):
        warnings.warn(
            (
                'Constraint of type {constraint_name} only accepts values that meet the following requirements: '
                '{value_allowed}. Value found: "{value_found}". '
                'Constrained will *not* be stored.'
            ).format(
                constraint_name=constraint_name,
                value_allowed=', '.join(value_allowed),
                value_found=value_found
            ),
            ConstraintValueWarning
        )
