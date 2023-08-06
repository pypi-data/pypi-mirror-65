# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access, bad-continuation

# import general packages
import unittest
import os
from lxml import objectify

from ..proto_builder import ProtoBuilder
from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.data_type_definition import DataTypeDefinition


class TestProtoBuilderDataTypeEvaluation(unittest.TestCase):

    def setUp(self) -> None:

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__), 'fdl', 'Simple.sila.xml'))
        self.proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

    def test_simple_basic(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_BASIC

        for basic_type in DATA_BASIC:
            with self.subTest(basic_type=basic_type):
                obj = DataTypeDefinition(
                    xml_tree_element=objectify.fromstring(DATA_BASIC[basic_type]).DataTypeDefinition
                )

                (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                                   identifier=obj.identifier,
                                                                                   namespace='sila2.main')

                self.assertIsNone(definition)
                self.assertEqual(
                    type_string,
                    "sila2.org.silastandard." + basic_type + " ${identifier} = ${index};"
                )

    def test_simple_list(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_LIST

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_LIST).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')
        self.assertIsNone(definition)
        self.assertEqual(
            type_string,
            "repeated sila2.org.silastandard.Boolean ${identifier} = ${index};"
        )

    def test_simple_constrained(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_CONSTRAINED_BASIC, DATA_CONSTRAINED_LIST

        with self.subTest(sub_type="BasicType"):
            obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_CONSTRAINED_BASIC).DataTypeDefinition)

            (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                               identifier=obj.identifier,
                                                                               namespace='sila2.main')
            self.assertIsNone(definition)
            self.assertEqual(
                type_string,
                (
                    "// Constrained type, not reflected in protocol buffers" "\n"
                    "sila2.org.silastandard.Boolean ${identifier} = ${index};"
                )
            )

        with self.subTest(sub_type="ListType"):
            obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_CONSTRAINED_LIST).DataTypeDefinition)

            (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                               identifier=obj.identifier,
                                                                               namespace='sila2.main')
            self.assertIsNone(definition)
            self.assertEqual(
                type_string,
                (
                    "// Constrained type, not reflected in protocol buffers" "\n"
                    "repeated sila2.org.silastandard.Boolean ${identifier} = ${index};"
                )
            )

    def test_simple_structure(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_STRUCTURE

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_STRUCTURE).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertIsNotNone(definition)
        self.assertEqual(
            definition,
            (
                "message StructureIdentifier_Struct {" "\n"
                "    " "// Basic Element" "\n"
                "    " "//   This parameter defines a basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement = 1;" "\n"
                "}"
            )
        )
        self.assertEqual(
            type_string,
            "sila2.main.StructureIdentifier_Struct ${identifier} = ${index};"
        )

    def test_simple_structure_multi(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_MULTI_STRUCTURE

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_MULTI_STRUCTURE).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertEqual(
            definition,
            (
                "message StructureIdentifier_Struct {" "\n"
                "    " "// 1. Basic Element" "\n"
                "    " "//   This parameter defines a 1. basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement1 = 1;" "\n"
                "    " "// 2. Basic Element" "\n"
                "    " "//   This parameter defines a 2. basic element." "\n"
                "    " "sila2.org.silastandard.Boolean BasicElement2 = 2;" "\n"
                "}"
            )
        )
        self.assertEqual(
            type_string,
            "sila2.main.StructureIdentifier_Struct ${identifier} = ${index};"
        )

    def test_simple_data_type_identifier(self):
        from ._data_proto_builder__data_type_definition_simple import DATA_DATA_TYPE_IDENTIFIER

        obj = DataTypeDefinition(xml_tree_element=objectify.fromstring(DATA_DATA_TYPE_IDENTIFIER).DataTypeDefinition)

        (definition, type_string) = self.proto_builder._evaluate_data_type(data_type=obj.sub_type,
                                                                           identifier=obj.identifier,
                                                                           namespace='sila2.main')

        self.assertIsNone(definition)
        self.assertEqual(
            type_string,
            "${namespace}.DataType_TestDataType ${identifier} = ${index};"
        )
