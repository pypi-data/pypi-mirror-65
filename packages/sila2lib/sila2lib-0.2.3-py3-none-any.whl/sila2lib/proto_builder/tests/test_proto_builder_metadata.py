# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general packages
import unittest
import os

from ..proto_builder import ProtoBuilder
from ...fdl_parser.fdl_parser import FDLParser


class TestProtoBuilderMetadata(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_simple_generate_message(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Metadata_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'MetadataIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            prefix='Metadata_',
            postfix='',
            data_types={
                identifier: fdl_parser.metadata[identifier].parameter
            }
        )

        self.assertEqual(
            code_content,
            (
                "message Metadata_MetadataIdentifier {" "\n"
                "    " "sila2.org.silastandard.Boolean MetadataIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_metadata_calls(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Metadata_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'MetadataIdentifier'

        code_content = proto_builder._generate_metadata_calls(metadata=fdl_parser.metadata[identifier])

        self.assertEqual(
            code_content,
            (
                "// Metadata Name" "\n"
                "//   This is a metadata element." "\n"
                "rpc Get_FCPAffectedByMetadata_MetadataIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.Get_FCPAffectedByMetadata_MetadataIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.Get_FCPAffectedByMetadata_MetadataIdentifier_Responses) {}"
            )
        )

    def test_simple_generate_metadata_message(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Metadata_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'MetadataIdentifier'

        code_content = proto_builder._generate_metadata_messages(metadata=fdl_parser.metadata[identifier])

        self.assertEqual(
            code_content,
            (
                'message Get_FCPAffectedByMetadata_MetadataIdentifier_Parameters {}' '\n'
                'message Get_FCPAffectedByMetadata_MetadataIdentifier_Responses {' '\n'
                '    ' 'repeated sila2.org.silastandard.String AffectedCalls = 1;' '\n'
                '}'
            )
        )
