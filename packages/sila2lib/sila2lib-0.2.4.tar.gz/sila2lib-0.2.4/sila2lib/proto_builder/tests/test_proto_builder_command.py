# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access, bad-continuation

# import general packages
import unittest
import os

from ..proto_builder import ProtoBuilder
from ...fdl_parser.fdl_parser import FDLParser


class TestProtoBuilderCommands(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None  # pylint: disable=invalid-name

    def test_simple_generate_parameter(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Parameters',
            data_types=fdl_parser.commands[identifier].parameters)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Responses',
            data_types=fdl_parser.commands[identifier].responses)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_simple_no_response_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Simple_No-Response.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Responses',
            data_types=fdl_parser.commands[identifier].responses)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Responses {" "\n"
                "    " "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_parameter_multi(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_SimpleMulti.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Parameters',
            data_types=fdl_parser.commands[identifier].parameters)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier1 = 1;" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier2 = 2;" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_response_multi(self):
        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_SimpleMulti.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Responses',
            data_types=fdl_parser.commands[identifier].responses)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier1 = 1;" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier2 = 2;" "\n"
                "}" "\n"
            )
        )

    def test_observable_no_intermediate_generate_parameter(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_NoIntermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Parameters',
            data_types=fdl_parser.commands[identifier].parameters)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_observable_no_intermediate_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_NoIntermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Responses',
            data_types=fdl_parser.commands[identifier].responses)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_observable_intermediate_generate_parameter(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_Intermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Parameters',
            data_types=fdl_parser.commands[identifier].parameters)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_observable_intermediate_generate_response(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_Intermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_Responses',
            data_types=fdl_parser.commands[identifier].responses)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_observable_intermediate_generate_intermediate(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_Intermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_arguments(
            identifier=identifier,
            postfix='_IntermediateResponses',
            data_types=fdl_parser.commands[identifier].intermediates)

        self.assertEqual(
            code_content,
            (
                "message CommandIdentifier_IntermediateResponses {" "\n"
                "    " "sila2.org.silastandard.Boolean IntermediateResponseIdentifier = 1;" "\n"
                "}" "\n"
            )
        )

    def test_simple_generate_command_calls(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_calls(command=fdl_parser.commands[identifier])

        self.assertEqual(
            code_content,
            (
                "// Command Name" "\n"
                "//   This is a simple, unobservable command." "\n"
                "rpc CommandIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
            )
        )

    def test_simple_generate_command_calls_multi(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_SimpleMulti.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_calls(command=fdl_parser.commands[identifier])

        self.assertEqual(
            code_content,
            (
                "// Command Name" "\n"
                "//   This is a simple, unobservable command." "\n"
                "rpc CommandIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
            )
        )

    def test_observable_no_intermediate_generate_command_calls(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_NoIntermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_calls(command=fdl_parser.commands[identifier])

        self.assertEqual(
            code_content,
            (
                "// Command Name" "\n"
                "//   This is an observable command without any intermediates." "\n" +
                (
                    "rpc CommandIdentifier"
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                    " returns "
                    "(sila2.org.silastandard.CommandConfirmation) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Info"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(stream sila2.org.silastandard.ExecutionInfo) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Result"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
                )
            )
        )

    def test_observable_intermediate_generate_command_calls(self):
        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_Intermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)

        # set the identifier of the command manually (see corresponding xml file)
        identifier = 'CommandIdentifier'

        code_content = proto_builder._generate_command_calls(command=fdl_parser.commands[identifier])

        self.assertEqual(
            code_content,
            (
                    "// Command Name" "\n"
                    "//   This is an observable command including intermediate responses." "\n" +
                    (
                        "rpc CommandIdentifier"
                        "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                        " returns "
                        "(sila2.org.silastandard.CommandConfirmation) {}"
                    ) + "\n" + (
                        "rpc CommandIdentifier_Intermediate"
                        "(sila2.org.silastandard.CommandExecutionUUID)"
                        " returns "
                        "(stream sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_IntermediateResponses) {}"
                    ) + "\n" + (
                        "rpc CommandIdentifier_Info"
                        "(sila2.org.silastandard.CommandExecutionUUID)"
                        " returns "
                        "(stream sila2.org.silastandard.ExecutionInfo) {}"
                    ) + "\n" + (
                        "rpc CommandIdentifier_Result"
                        "(sila2.org.silastandard.CommandExecutionUUID)"
                        " returns "
                        "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
                    )
            )
        )

    def test_simple_create_commands(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Simple.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        code_rpc, code_parameters = proto_builder._create_commands()

        self.assertEqual(
            code_rpc,
            (
                "// Command Name" "\n"
                "//   This is a simple, unobservable command." "\n"
                "rpc CommandIdentifier"
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                " returns "
                "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
            )
        )

        self.assertEqual(
            code_parameters,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
                "\n"
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}"
            )
        )

    def test_observable_no_intermediate_create_commands(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_NoIntermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        code_rpc, code_parameters = proto_builder._create_commands()

        self.assertEqual(
            code_rpc,
            (
                "// Command Name" "\n"
                "//   This is an observable command without any intermediates." "\n" +
                (
                    "rpc CommandIdentifier"
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                    " returns "
                    "(sila2.org.silastandard.CommandConfirmation) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Info"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(stream sila2.org.silastandard.ExecutionInfo) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Result"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
                )
            )
        )

        self.assertEqual(
            code_parameters,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
                "\n"
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}"
            )
        )

    def test_observable_intermediate_create_commands(self):

        # set up the ProtoBuilder object used for the validation
        fdl_parser = FDLParser(fdl_filename=os.path.join(os.path.dirname(__file__),
                                                         'fdl',
                                                         'Command_Observable_Intermediate.sila.xml')
                               )
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        code_rpc, code_parameters = proto_builder._create_commands()

        self.assertEqual(
            code_rpc,
            (
                "// Command Name" "\n"
                "//   This is an observable command including intermediate responses." "\n" +
                (
                    "rpc CommandIdentifier"
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Parameters)"
                    " returns "
                    "(sila2.org.silastandard.CommandConfirmation) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Intermediate"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(stream sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_IntermediateResponses) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Info"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(stream sila2.org.silastandard.ExecutionInfo) {}"
                ) + "\n" + (
                    "rpc CommandIdentifier_Result"
                    "(sila2.org.silastandard.CommandExecutionUUID)"
                    " returns "
                    "(sila2.org.silastandard.none.simplefeature.v1.CommandIdentifier_Responses) {}"
                )
            )
        )

        self.assertEqual(
            code_parameters,
            (
                "message CommandIdentifier_Parameters {" "\n"
                "    " "sila2.org.silastandard.Boolean ParameterIdentifier = 1;" "\n"
                "}" "\n"
                "\n"
                "message CommandIdentifier_Responses {" "\n"
                "    " "sila2.org.silastandard.Boolean ResponseIdentifier = 1;" "\n"
                "}" "\n"
                "\n"
                "message CommandIdentifier_IntermediateResponses {" "\n"
                "    " "sila2.org.silastandard.Boolean IntermediateResponseIdentifier = 1;" "\n"
                "}"
            )
        )
