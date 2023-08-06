# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..standard_errors import StandardError, DefinedExecutionError


class TestStandardError(unittest.TestCase):
    """
    This unittest tests the :class:`~..StandardError` class.
        Theoretically we would need to test the class :class:`DefinedExecutionError`, however,
        since they are simply derived from the base class without any changes we simply go for the base class and only
        once construct the derived types to have them covered.
    """

    def setUp(self):
        # define the patterns which we expect to read for the different errors
        self.defined_error_identifier = "ExecutionError{count}"
        self.defined_error_display_name = "Execution Error {count}"
        self.defined_error_description = "{count}. error that can occur when executing a command or reading a property."

    def test_tree(self):
        from ._data_standard_errors import DATA_DEFINED_EXECUTION_ERROR

        with self.subTest(error_type="DefinedExecutionError"):
            xml_input = objectify.fromstring(DATA_DEFINED_EXECUTION_ERROR)
            for standard_error in xml_input.DefinedExecutionError:
                obj = StandardError(xml_tree_element=standard_error)

                self.assertEqual(standard_error, obj._tree)

    def test_attributes(self):
        from ._data_standard_errors import DATA_DEFINED_EXECUTION_ERROR

        with self.subTest(error_type="DefinedExecutionError"):
            xml_input = objectify.fromstring(DATA_DEFINED_EXECUTION_ERROR)
            for counter, standard_error in enumerate(xml_input.DefinedExecutionError, start=1):
                obj = StandardError(xml_tree_element=standard_error)

                self.assertEqual(self.defined_error_identifier.format(count=counter), obj.identifier)
                self.assertEqual(self.defined_error_display_name.format(count=counter), obj.name)
                self.assertEqual(self.defined_error_description.format(count=counter), obj.description)

    def test_defined_execution_error(self):
        from ._data_standard_errors import DATA_DEFINED_EXECUTION_ERROR

        xml_input = objectify.fromstring(DATA_DEFINED_EXECUTION_ERROR)
        obj = DefinedExecutionError(xml_tree_element=xml_input.DefinedExecutionError[0])

        self.assertIsInstance(obj, StandardError)
        self.assertIsInstance(obj, DefinedExecutionError)
