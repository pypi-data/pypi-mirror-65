# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..type_list import ListType
from ..type_basic import BasicType
from ..type_structured import StructureType
from ..type_constrained import ConstrainedType
from ..type_data_type_identifier import DataTypeIdentifier

# import custom exceptions
from ..exceptions.exceptions import SubDataTypeError


class TestListType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_basic(self):
        from ._data_type_list import DATA_BASIC

        obj = ListType(objectify.fromstring(DATA_BASIC).List)
        self.assertIs(type(obj.sub_type), BasicType)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_list)

    def test_list(self):
        from ._data_type_list import DATA_LIST

        # List of lists are not allowed
        with self.assertRaises(SubDataTypeError):
            _ = ListType(objectify.fromstring(DATA_LIST).List)

    def test_structure(self):
        from ._data_type_list import DATA_STRUCTURE

        obj = ListType(objectify.fromstring(DATA_STRUCTURE).List)
        self.assertIs(type(obj.sub_type), StructureType)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_list)

    def test_constrained(self):
        from ._data_type_list import DATA_CONSTRAINED

        obj = ListType(objectify.fromstring(DATA_CONSTRAINED).List)
        self.assertIs(type(obj.sub_type), ConstrainedType)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_list)

    def test_data_type_identifier(self):
        from ._data_type_list import DATA_DATA_TYPE_IDENTIFIER

        obj = ListType(objectify.fromstring(DATA_DATA_TYPE_IDENTIFIER).List)
        self.assertIs(type(obj.sub_type), DataTypeIdentifier)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_list)
