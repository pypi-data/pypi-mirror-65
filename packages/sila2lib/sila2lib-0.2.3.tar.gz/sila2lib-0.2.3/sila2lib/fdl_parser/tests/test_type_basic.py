# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..type_basic import BasicType


class TestBasicType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_sila_types(self):
        from ._data_type_basic import DATA_SILA_STANDARD_TYPES

        data_types = ['Boolean', 'Integer', 'Real', 'String', 'Binary', 'Void', 'Date', 'Time', 'Timestamp']
        data_type_classes = [bool, int, float, str, bytes, bytes, str, str, str]

        for data_type, data_type_class in zip(data_types, data_type_classes):
            with self.subTest(data_type=data_type):
                # create the object
                obj = BasicType(xml_tree_element=objectify.fromstring(DATA_SILA_STANDARD_TYPES[data_type]).Basic)

                # correct type extracted
                self.assertEqual(obj.sub_type, data_type)
                # correct name
                self.assertEqual(obj.name, data_type)
                # is marked as basic
                self.assertTrue(obj.is_basic)
                # default value must be acceptable type
                self.assertIs(type(obj.default_value), data_type_class)
