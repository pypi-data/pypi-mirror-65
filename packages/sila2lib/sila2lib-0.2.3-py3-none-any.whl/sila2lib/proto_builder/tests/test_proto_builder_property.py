# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general packages
import unittest
import os

from sila2lib.proto_builder.proto_builder import ProtoBuilder
from sila2lib.fdl_parser.fdl_parser import FDLParser


class TestProtoBuilderProperties(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_simple_generate_parameter(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Simple.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            prefix='Get_',
            postfix='_Parameters',
            data_types={})

        self.assertEqual(
            code_content,
            (
                "message Get_PropertyIdentifier_Parameters {" "\n"
                "    " "// Empty message" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Simple.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            prefix='Get_',
            postfix='_Responses',
            data_types={
                identifier: fdl_parser.properties[identifier].response
            }
        )

        self.assertEqual(
            code_content,
            (
                "message Get_PropertyIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean PropertyIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_observable_generate_parameter(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Observable.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            prefix='Subscribe_',
            postfix='_Parameters',
            data_types={})

        self.assertEqual(
            code_content,
            (
                "message Subscribe_PropertyIdentifier_Parameters {" "\n"
                "    " "// Empty message" "\n"
                "}" "\n"
            )
        )

    def test_observable_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Observable.sila.xml'))
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            prefix='Subscribe_',
            postfix='_Responses',
            data_types={
                identifier: fdl_parser.properties[identifier].response
            }
        )

        self.assertEqual(
            code_content,
            (
                "message Subscribe_PropertyIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean PropertyIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_property_calls(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_property_calls(fdl_property=fdl_parser.properties[identifier])

        self.assertEqual(
            code_content,
            (
                "// Property Name" "\n"
                "//   This is a simple, unobservable property." "\n"
                "rpc Get_PropertyIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.Get_PropertyIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.Get_PropertyIdentifier_Responses) {}"
            )
        )

    def test_observable_generate_property_calls(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Observable.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'PropertyIdentifier'

        code_content = proto_builder._generate_property_calls(fdl_property=fdl_parser.properties[identifier])

        self.assertEqual(
            code_content,
            (
                "// Property Name" "\n"
                "//   This is an observable property." "\n"
                "rpc Subscribe_PropertyIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.Subscribe_PropertyIdentifier_Parameters)"
                " returns "
                "(stream sila2.org.silastandard.none.simplefeature.v1.Subscribe_PropertyIdentifier_Responses) {}"
            )
        )

    def test_simple_create_properties(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        code_rpc, code_parameters = proto_builder._create_properties()

        self.assertEqual(
            code_rpc,
            (
                "// Property Name" "\n"
                "//   This is a simple, unobservable property." "\n"
                "rpc Get_PropertyIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.Get_PropertyIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.Get_PropertyIdentifier_Responses) {}"
            )
        )

        self.assertEqual(
            code_parameters,
            (
                "message Get_PropertyIdentifier_Parameters {" "\n"
                "    " "// Empty message" "\n"
                "}" "\n"
                "\n"
                "message Get_PropertyIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean PropertyIdentifier = 1;" "\n"
                "}"
            )
        )

    def test_observable_create_properties(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Property_Observable.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        code_rpc, code_parameters = proto_builder._create_properties()

        self.assertEqual(
            code_rpc,
            (
                "// Property Name" "\n"
                "//   This is an observable property." "\n" +
                "rpc Subscribe_PropertyIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.Subscribe_PropertyIdentifier_Parameters)"
                " returns "
                "(stream sila2.org.silastandard.none.simplefeature.v1.Subscribe_PropertyIdentifier_Responses) {}"
            )
        )

        self.assertEqual(
            code_parameters,
            (
                "message Subscribe_PropertyIdentifier_Parameters {" "\n"
                "    " "// Empty message" "\n"
                "}" "\n"
                "\n"
                "message Subscribe_PropertyIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean PropertyIdentifier = 1;" "\n"
                "}"
            )
        )
