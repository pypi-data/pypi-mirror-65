# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..property import Property
from ..data_type_response import ResponseDataType


class TestProperty(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_tree(self):
        from ._data_property import DATA_SIMPLE

        xml_input = objectify.fromstring(DATA_SIMPLE).Property
        obj = Property(xml_tree_element=xml_input)

        self.assertEqual(xml_input, obj._tree)

    def test_attributes(self):
        from ._data_property import DATA_SIMPLE

        obj = Property(xml_tree_element=objectify.fromstring(DATA_SIMPLE).Property)
        # check simple attributes
        self.assertEqual(
            obj.identifier,
            "PropertyIdentifier"
        )
        self.assertEqual(
            obj.name,
            "Property Name"
        )
        self.assertEqual(
            obj.description,
            "Simple, unobservable property"
        )
        self.assertFalse(obj.observable)
        # check parameter and responses
        self.assertIs(type(obj.response), ResponseDataType)

    def test_observable(self):
        from ._data_property import DATA_OBSERVABLE

        obj = Property(xml_tree_element=objectify.fromstring(DATA_OBSERVABLE).Property)
        self.assertTrue(obj.observable)

    def test_defined_execution_errors(self):
        from ._data_property import DATA_DEFINED_EXECUTION_ERRORS

        obj = Property(xml_tree_element=objectify.fromstring(DATA_DEFINED_EXECUTION_ERRORS).Property)

        self.assertEqual(len(obj.defined_execution_errors), 3)
        for index in range(1, 3):
            identifier = "ReadError{index}".format(index=index)
            self.assertIn(identifier, obj.defined_execution_errors)
