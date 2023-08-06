# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
import os

# import package related modules and classes
from ..fdl_parser import FDLParser
from ..command import Command
from ..property import Property
from ..data_type_definition import DataTypeDefinition
from ..standard_errors import DefinedExecutionError


class TestFDLParser(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        Create the basic path in which the input xml files are stored.
        """
        self.base_path = os.path.join(os.path.dirname(__file__), "fdl")

    def test_feature(self):
        obj = FDLParser(os.path.join(self.base_path, "Simple.sila.xml"))

        self.assertEqual(obj.root.tag, '{http://www.sila-standard.org}Feature')

    def test_attributes(self):
        """
        Test of all attributes are read correctly
            For this test it is assumed that no optional attributes are present and only default values are found.
        """
        obj = FDLParser(os.path.join(self.base_path, "Simple.sila.xml"))

        # start with mandatory attributes
        self.assertEqual(obj.feature_version, '1.3')
        self.assertEqual(obj.feature_version_major, 1)
        self.assertEqual(obj.feature_version_minor, 3)
        self.assertEqual(obj.originator, 'org.silastandard')
        self.assertEqual(obj.sila2_version, '1.0')
        # optional arguments and defaults
        self.assertEqual(obj.maturity_level, 'Draft')
        self.assertEqual(obj.category, 'example')
        self.assertEqual(obj.locale, 'en-us')

    def test_attributes_optional(self):
        """
        Tests if optional attributes are read correctly if not set.
            For this test all optional attributes must be set.
        """
        obj = FDLParser(os.path.join(self.base_path, "Simple_AttributesOptional.sila.xml"))
        self.assertEqual(obj.locale, 'en-us')
        self.assertEqual(obj.maturity_level, 'Draft')

    def test_elements_base(self):
        """Tests if the base elements of a feature are read correctly."""
        obj = FDLParser(os.path.join(self.base_path, "Simple.sila.xml"))

        self.assertEqual(obj.identifier, 'SimpleFeature')
        self.assertEqual(obj.name, 'Simple Feature')
        self.assertEqual(
            obj.description,
            'Minimal feature definition, nothing is required. Can be used to check (default) attributes.'
        )

    def test_elements_complete(self):
        """Tests if all elements (one of each) are read correctly."""
        obj = FDLParser(os.path.join(self.base_path, "Complete.sila.xml"))

        self.assertEqual(len(obj.commands), 1)
        self.assertIn('CommandIdentifier', obj.commands)
        self.assertIs(type(obj.commands['CommandIdentifier']), Command)

        self.assertEqual(len(obj.properties), 1)
        self.assertIn('PropertyIdentifier', obj.properties)
        self.assertIs(type(obj.properties['PropertyIdentifier']), Property)

        self.assertEqual(len(obj.data_type_definitions), 1)
        self.assertIn('DataTypeDefinitionIdentifier', obj.data_type_definitions)
        self.assertIs(type(obj.data_type_definitions['DataTypeDefinitionIdentifier']), DataTypeDefinition)

        self.assertEqual(len(obj.defined_execution_errors), 1)
        self.assertIn('DefinedExecutionErrorIdentifier', obj.defined_execution_errors)
        self.assertIs(type(obj.defined_execution_errors['DefinedExecutionErrorIdentifier']), DefinedExecutionError)
