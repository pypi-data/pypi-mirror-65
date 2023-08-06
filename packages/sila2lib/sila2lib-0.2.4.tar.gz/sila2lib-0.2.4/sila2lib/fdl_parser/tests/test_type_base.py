# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..type_basic import BasicType


class TestDataType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_tree(self):
        from ._data_type_basic import DATA_BOOLEAN
        obj = BasicType(objectify.fromstring(DATA_BOOLEAN).Basic)

        self.assertEqual(objectify.fromstring(DATA_BOOLEAN).Basic, obj._tree)
