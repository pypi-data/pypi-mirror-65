# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..data_type_definition import DataTypeDefinition
from ..type_basic import BasicType
from ..type_list import ListType
from ..type_structured import StructureType
from ..type_constrained import ConstrainedType
from ..type_data_type_identifier import DataTypeIdentifier


class TestDataTypeDefinition(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_basic(self):
        from ._data_data_type_definition import DATA_BASIC

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_BASIC).DataTypeDefinition)
        self.assertIs(type(obj.sub_type), BasicType)
        self.assertEqual(
            obj.description,
            "Definition of an identifier for a basic data type"
        )
        self.assertEqual(
            obj.name,
            "Basic Identifier"
        )
        self.assertEqual(
            obj.identifier,
            "BasicIdentifier"
        )

    def test_list(self):
        from ._data_data_type_definition import DATA_LIST

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_LIST).DataTypeDefinition)
        self.assertIs(type(obj.sub_type), ListType)
        self.assertEqual(
            obj.description,
            "Definition of an identifier for a list data type"
        )
        self.assertEqual(
            obj.name,
            "List Identifier"
        )
        self.assertEqual(
            obj.identifier,
            "ListIdentifier"
        )

    def test_structure(self):
        from ._data_data_type_definition import DATA_STRUCTURE

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_STRUCTURE).DataTypeDefinition)
        self.assertIs(type(obj.sub_type), StructureType)
        self.assertEqual(
            obj.description,
            "Definition of an identifier for a structure data type"
        )
        self.assertEqual(
            obj.name,
            "Structure Identifier"
        )
        self.assertEqual(
            obj.identifier,
            "StructureIdentifier"
        )

    def test_constrained(self):
        from ._data_data_type_definition import DATA_CONSTRAINED

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_CONSTRAINED).DataTypeDefinition)
        self.assertIs(type(obj.sub_type), ConstrainedType)
        self.assertEqual(
            obj.description,
            "Definition of an identifier for a constrained data type"
        )
        self.assertEqual(
            obj.name,
            "Constrained Identifier"
        )
        self.assertEqual(
            obj.identifier,
            "ConstrainedIdentifier"
        )

    def test_data_type_identifier(self):
        from ._data_data_type_definition import DATA_DATA_TYPE_IDENTIFIER

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_DATA_TYPE_IDENTIFIER).DataTypeDefinition)
        self.assertIs(type(obj.sub_type), DataTypeIdentifier)
        self.assertEqual(
            obj.description,
            "Definition of an identifier for a defined data type"
        )
        self.assertEqual(
            obj.name,
            "Definition Identifier"
        )
        self.assertEqual(
            obj.identifier,
            "DefinitionIdentifier"
        )
