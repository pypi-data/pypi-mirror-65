# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from itertools import product
from lxml import objectify

# import package related modules and classes
from ..type_list import ListType
from ..type_basic import BasicType
from ..type_structured import StructureType
from ..type_constrained import ConstrainedType
from ..type_data_type_identifier import DataTypeIdentifier

from ._data_type_structured import data_structure_arbitrary


class TestStructureType(unittest.TestCase):

    #: The maximum count of sub-elements
    max_count: int = 5

    #: The maximum number of combinations that are tested
    max_count_combinations: int = 4

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.
            Pre-loads all element strings used to construct arbitrary structures.
        """
        # (pre-)load the element strings to have easier access in the test methods
        from ._data_type_structured import DATA_BASIC_ELEMENT, DATA_LIST_ELEMENT, \
            DATA_STRUCTURE_ELEMENT, DATA_CONSTRAINED_ELEMENT, DATA_DATA_TYPE_IDENTIFIER_ELEMENT
        self.element_strings = {
            'basic':                DATA_BASIC_ELEMENT,
            'list':                 DATA_LIST_ELEMENT,
            'structure':            DATA_STRUCTURE_ELEMENT,
            'constrained':          DATA_CONSTRAINED_ELEMENT,
            'data_type_identifier': DATA_DATA_TYPE_IDENTIFIER_ELEMENT
        }
        self.types = {
            'basic':                BasicType,
            'list':                 ListType,
            'structure':            StructureType,
            'constrained':          ConstrainedType,
            'data_type_identifier': DataTypeIdentifier
        }

    def test_basic(self):
        # define the key for the dictionaries prepared in setUp() to access the correct strings and types
        test_key = 'basic'

        # construct structures of different length with the same elements and check them all
        for element_count in range(1, self.max_count):
            with self.subTest(element_count=element_count):
                input_list = [self.element_strings[test_key]] * element_count
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), element_count)
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type and the identifier, description and name have been
                #   read
                for index in range(0, element_count-1):
                    with self.subTest(element_id=index, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[test_key])
                    with self.subTest(element_id=index, test="Identifier"):
                        self.assertEqual(
                            obj.sub_type[index].identifier,
                            "StructureElement_{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="DisplayName"):
                        self.assertEqual(
                            obj.sub_type[index].name,
                            "Structure Element #{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="Description"):
                        self.assertEqual(
                            obj.sub_type[index].description,
                            "This parameter defines the {count}. element of a structure.".format(count=index+1)
                        )

    def test_list(self):
        # define the key for the dictionaries prepared in setUp() to access the correct strings and types
        test_key = 'list'

        # construct structures of different length with the same elements and check them all
        for element_count in range(1, self.max_count):
            with self.subTest(element_count=element_count):
                input_list = [self.element_strings[test_key]] * element_count
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), element_count)
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type and the identifier, description and name have been
                #   read
                for index in range(0, element_count-1):
                    with self.subTest(element_id=index, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[test_key])
                    with self.subTest(element_id=index, test="Identifier"):
                        self.assertEqual(
                            obj.sub_type[index].identifier,
                            "StructureElement_{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="DisplayName"):
                        self.assertEqual(
                            obj.sub_type[index].name,
                            "Structure Element #{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="Description"):
                        self.assertEqual(
                            obj.sub_type[index].description,
                            "This parameter defines the {count}. element of a structure.".format(count=index+1)
                        )

    def test_structure(self):
        # define the key for the dictionaries prepared in setUp() to access the correct strings and types
        test_key = 'structure'

        # construct structures of different length with the same elements and check them all
        for element_count in range(1, self.max_count):
            with self.subTest(element_count=element_count):
                input_list = [self.element_strings[test_key]] * element_count
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), element_count)
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type and the identifier, description and name have been
                #   read
                for index in range(0, element_count-1):
                    with self.subTest(element_id=index, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[test_key])
                    with self.subTest(element_id=index, test="Identifier"):
                        self.assertEqual(
                            obj.sub_type[index].identifier,
                            "StructureElement_{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="DisplayName"):
                        self.assertEqual(
                            obj.sub_type[index].name,
                            "Structure Element #{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="Description"):
                        self.assertEqual(
                            obj.sub_type[index].description,
                            "This parameter defines the {count}. element of a structure.".format(count=index+1)
                        )

    def test_constrained(self):
        # define the key for the dictionaries prepared in setUp() to access the correct strings and types
        test_key = 'constrained'

        # construct structures of different length with the same elements and check them all
        for element_count in range(1, self.max_count):
            with self.subTest(element_count=element_count):
                input_list = [self.element_strings[test_key]] * element_count
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), element_count)
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type and the identifier, description and name have been
                #   read
                for index in range(0, element_count-1):
                    with self.subTest(element_id=index, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[test_key])
                    with self.subTest(element_id=index, test="Identifier"):
                        self.assertEqual(
                            obj.sub_type[index].identifier,
                            "StructureElement_{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="DisplayName"):
                        self.assertEqual(
                            obj.sub_type[index].name,
                            "Structure Element #{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="Description"):
                        self.assertEqual(
                            obj.sub_type[index].description,
                            "This parameter defines the {count}. element of a structure.".format(count=index+1)
                        )

    def test_data_type_identifier(self):
        # define the key for the dictionaries prepared in setUp() to access the correct strings and types
        test_key = 'data_type_identifier'

        # construct structures of different length with the same elements and check them all
        for element_count in range(1, self.max_count):
            with self.subTest(element_count=element_count):
                input_list = [self.element_strings[test_key]] * element_count
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), element_count)
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type and the identifier, description and name have been
                #   read
                for index in range(0, element_count-1):
                    with self.subTest(element_id=index, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[test_key])
                    with self.subTest(element_id=index, test="Identifier"):
                        self.assertEqual(
                            obj.sub_type[index].identifier,
                            "StructureElement_{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="DisplayName"):
                        self.assertEqual(
                            obj.sub_type[index].name,
                            "Structure Element #{count}".format(count=index+1)
                        )
                    with self.subTest(element_id=index, test="Description"):
                        self.assertEqual(
                            obj.sub_type[index].description,
                            "This parameter defines the {count}. element of a structure.".format(count=index+1)
                        )

    def test_permutations(self):
        """
        This test tests all combinations of up to `max_count_combinations` sub-elements of a structure.

        .. note:: Since all possible combinations are used, this can produce a very long list of combinations that are
                  being tested and thus take a while. If it takes to long, reduce the number of combinations by
                  adjusting `max_count_combinations`.
        """
        # create combinations of the sub-elements
        combinations = product(self.element_strings.keys(), repeat=self.max_count_combinations)

        for combination in combinations:
            with self.subTest(combination=list(combination)):
                input_list = [self.element_strings[item] for item in combination]
                input_structure = data_structure_arbitrary(*input_list)

                obj = StructureType(objectify.fromstring(input_structure).Structure)

                # first check if the total length of elements read is correct
                self.assertEqual(len(obj.sub_type), len(combination))
                self.assertTrue(obj.is_structure)

                # make sure each sub-element is of the correct type
                for index, element_type in enumerate(combination, 0):
                    with self.subTest(element=element_type, test="type()"):
                        self.assertIs(type(obj.sub_type[index].sub_type), self.types[element_type])
