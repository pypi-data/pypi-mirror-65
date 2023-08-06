# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access, redundant-unittest-assert

# import general Packages
import unittest
import os

# import package related modules and classes
from ..fdl_validator import FDLValidator


class TestFDLValidator(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        Create the basic path in which the input xml files are stored.
        """
        self.base_path = os.path.join(os.path.dirname(__file__), "fdl")

    def test_simple(self):
        obj = FDLValidator()
        self.assertTrue(obj.validate(os.path.join(self.base_path, 'Simple.sila.xml')))

    @unittest.skip('This test would require a xml file that contains all possible definitions, especially Data Types '
                   'and a lot of nesting.')
    def test_complete(self):
        self.assertTrue(False)

    @unittest.skip('This test would require an invalid XML/FDL file. There are many possibilities to generate an '
                   'invalid file, and I do not know which possibilities are reasonable here.')
    def test_invalid(self):
        self.assertTrue(False)
