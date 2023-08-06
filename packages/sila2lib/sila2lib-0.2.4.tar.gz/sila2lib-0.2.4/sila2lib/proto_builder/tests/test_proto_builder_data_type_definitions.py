# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access, bad-continuation

# import general packages
import unittest
import os

from ..proto_builder import ProtoBuilder
from ...fdl_parser.fdl_parser import FDLParser


class TestProtoBuilderDataTypeDefinitions(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_simple_basic(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_Basic.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Basic Definition" "\n"
                "//   A definition of a basic data type" "\n"
                "message DataType_BasicDefinition {" "\n"
                "    " "sila2.org.silastandard.Boolean BasicDefinition = 1;" "\n"
                "}"
            )
        )

    def test_simple_list(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_List.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// List Definition" "\n"
                "//   A definition of a list data type" "\n"
                "message DataType_ListDefinition {" "\n"
                "    " "repeated sila2.org.silastandard.Boolean ListDefinition = 1;" "\n"
                "}"
            )
        )

    def test_simple_constrained(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_Constrained.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Constrained Definition" "\n"
                "//   A definition of a constrained data type" "\n"
                "message DataType_ConstrainedDefinition {" "\n"
                "    " "// Constrained type, not reflected in protocol buffers" "\n"
                "    " "sila2.org.silastandard.Boolean ConstrainedDefinition = 1;" "\n"
                "}"
            )
        )

    def test_simple_structure(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_Structure.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Structure Definition" "\n"
                "//   A definition of a structure data type" "\n"
                "message DataType_StructureDefinition {" "\n"
                "    " "message StructureDefinition_Struct {" "\n"
                "    " "    " "// Basic Element" "\n"
                "    " "    " "//   A basic element of the structure" "\n"
                "    " "    " "sila2.org.silastandard.Boolean BasicElement = 1;" "\n"
                "    " "}" "\n"
                "    " "sila2.org.silastandard.none.simplefeature.v1"
                       ".DataType_StructureDefinition.StructureDefinition_Struct" " "
                       "StructureDefinition = 1;" "\n"
                "}"
            )
        )

    def test_simple_structure_multi(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_StructureMulti.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Structure Definition" "\n"
                "//   A definition of a structure data type" "\n"
                "message DataType_StructureDefinition {" "\n"
                "    " "message StructureDefinition_Struct {" "\n"
                "    " "    " "// Basic Boolean Element" "\n"
                "    " "    " "//   A basic boolean element of the structure" "\n"
                "    " "    " "sila2.org.silastandard.Boolean BasicBooleanElement = 1;" "\n"
                "    " "    " "// Basic String Element" "\n"
                "    " "    " "//   A basic string element of the structure" "\n"
                "    " "    " "sila2.org.silastandard.String BasicStringElement = 2;" "\n"
                "    " "}" "\n"
                "    " "sila2.org.silastandard.none.simplefeature.v1"
                ".DataType_StructureDefinition.StructureDefinition_Struct" " "
                "StructureDefinition = 1;" "\n"
                "}"
            )
        )

    def test_structure_of_structure(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_StructureOfStructure.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Structure Definition" "\n"
                "//   A definition of a structure data type" "\n"
                "message DataType_StructureDefinition {" "\n"
                "    " "message StructureDefinition_Struct {" "\n"
                "    " "    " "message BasicElement_Struct {" "\n"
                "    " "    " "    " "// Sub Structure Element" "\n"
                "    " "    " "    " "//   Element of a structure in the second level" "\n"
                "    " "    " "    " "sila2.org.silastandard.Boolean SubStructureElement = 1;" "\n"
                "    " "    " "}" "\n"
                "    " "    " "// Basic Element" "\n"
                "    " "    " "//   A basic element of the structure" "\n"
                "    " "    " "sila2.org.silastandard.none.simplefeature.v1"
                              ".DataType_StructureDefinition.StructureDefinition_Struct.BasicElement_Struct" " "
                              "BasicElement = 1;" "\n"
                "    " "}" "\n"
                "    " "sila2.org.silastandard.none.simplefeature.v1"
                       ".DataType_StructureDefinition.StructureDefinition_Struct" " "
                       "StructureDefinition = 1;" "\n"
                "}"
            )
        )

    def test_structure_of_list(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_StructureOfList.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Structure Definition" "\n"
                "//   A definition of a structure data type" "\n"
                "message DataType_StructureDefinition {" "\n"
                "    " "message StructureDefinition_Struct {" "\n"
                "    " "    " "// Basic Element" "\n"
                "    " "    " "//   A basic element of the structure" "\n"
                "    " "    " "repeated sila2.org.silastandard.Boolean BasicElement = 1;" "\n"
                "    " "}" "\n"
                "    " "sila2.org.silastandard.none.simplefeature.v1"
                       ".DataType_StructureDefinition.StructureDefinition_Struct" " "
                       "StructureDefinition = 1;" "\n"
                "}"
            )
        )

    def test_simple_data_type_identifier(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'DataTypeDefinition_DataTypeIdentifier.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        code_content = proto_builder._create_data_types()

        self.assertEqual(
            code_content,
            (
                "// Identifier Definition" "\n"
                "//   A definition of an identifier data type" "\n"
                "message DataType_IdentifierDefinition {" "\n"
                "    " "sila2.org.silastandard.none.simplefeature.v1."
                       "DataType_TestDataType IdentifierDefinition = 1;" "\n"
                "}"
            )
        )
