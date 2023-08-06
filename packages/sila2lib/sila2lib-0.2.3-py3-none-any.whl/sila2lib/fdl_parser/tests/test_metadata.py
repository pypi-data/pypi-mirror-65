# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..metadata import Metadata
from ..data_type_parameter import ParameterDataType


class TestMetadata(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_tree(self):
        from ._data_metadata import DATA_SIMPLE

        xml_input = objectify.fromstring(DATA_SIMPLE).Metadata
        obj = Metadata(xml_tree_element=xml_input)

        self.assertEqual(xml_input, obj._tree)

    def test_attributes(self):
        from ._data_metadata import DATA_SIMPLE

        obj = Metadata(xml_tree_element=objectify.fromstring(DATA_SIMPLE).Metadata)
        # check simple attributes
        self.assertEqual(
            obj.identifier,
            "MetadataIdentifier"
        )
        self.assertEqual(
            obj.name,
            "Metadata Name"
        )
        self.assertEqual(
            obj.description,
            "Simple metadata element"
        )
        # check parameter and responses
        self.assertIs(type(obj.parameter), ParameterDataType)

    def test_defined_execution_errors(self):
        from ._data_metadata import DATA_DEFINED_EXECUTION_ERRORS

        obj = Metadata(xml_tree_element=objectify.fromstring(DATA_DEFINED_EXECUTION_ERRORS).Metadata)

        self.assertEqual(len(obj.defined_execution_errors), 3)
        for index in range(1, 3):
            identifier = "ExecutionError{index}".format(index=index)
            self.assertIn(identifier, obj.defined_execution_errors)
