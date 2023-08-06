# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..data_type_parameter import ParameterDataType
from ..type_basic import BasicType
from ..type_list import ListType
from ..type_structured import StructureType
from ..type_constrained import ConstrainedType
from ..type_data_type_identifier import DataTypeIdentifier


class TestParameterDataType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_basic(self):
        from ._data_data_type_parameter import DATA_BASIC

        obj = ParameterDataType(objectify.fromstring(DATA_BASIC).Parameter)
        self.assertIs(type(obj.sub_type), BasicType)
        self.assertEqual(
            obj.description,
            "This parameter defines a basic parameter."
        )
        self.assertEqual(
            obj.name,
            "Basic Parameter"
        )
        self.assertEqual(
            obj.identifier,
            "BasicParameter"
        )

    def test_list(self):
        from ._data_data_type_parameter import DATA_LIST

        obj = ParameterDataType(objectify.fromstring(DATA_LIST).Parameter)
        self.assertIs(type(obj.sub_type), ListType)
        self.assertEqual(
            obj.description,
            "This parameter defines a list parameter."
        )
        self.assertEqual(
            obj.name,
            "List Parameter"
        )
        self.assertEqual(
            obj.identifier,
            "ListParameter"
        )

    def test_structure(self):
        from ._data_data_type_parameter import DATA_STRUCTURE

        obj = ParameterDataType(objectify.fromstring(DATA_STRUCTURE).Parameter)
        self.assertIs(type(obj.sub_type), StructureType)
        self.assertEqual(
            obj.description,
            "This parameter defines a structure parameter."
        )
        self.assertEqual(
            obj.name,
            "Structure Parameter"
        )
        self.assertEqual(
            obj.identifier,
            "StructureParameter"
        )

    def test_constrained(self):
        from ._data_data_type_parameter import DATA_CONSTRAINED

        obj = ParameterDataType(objectify.fromstring(DATA_CONSTRAINED).Parameter)
        self.assertIs(type(obj.sub_type), ConstrainedType)
        self.assertEqual(
            obj.description,
            "This parameter defines a constrained parameter."
        )
        self.assertEqual(
            obj.name,
            "Constrained Parameter"
        )
        self.assertEqual(
            obj.identifier,
            "ConstrainedParameter"
        )

    def test_data_type_identifier(self):
        from ._data_data_type_parameter import DATA_DATA_TYPE_IDENTIFIER

        obj = ParameterDataType(objectify.fromstring(DATA_DATA_TYPE_IDENTIFIER).Parameter)
        self.assertIs(type(obj.sub_type), DataTypeIdentifier)
        self.assertEqual(
            obj.description,
            "This parameter defines a parameter that has been defined previously."
        )
        self.assertEqual(
            obj.name,
            "DefinedDataType Parameter"
        )
        self.assertEqual(
            obj.identifier,
            "DefinedDataType"
        )
