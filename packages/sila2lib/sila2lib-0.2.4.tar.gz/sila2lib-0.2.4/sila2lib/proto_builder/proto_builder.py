"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Protobuf file builder based on an FDL input.

:file:    proto_builder.py
:authors: Timm Severin

:date: (creation)          2019-08-20
:date: (last modification) 2019-11-02

__________________________________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
__________________________________________________________________________________________________
"""
# prepare logging
import logging

# import meta packages
from typing import Dict, List
from typing import Union

# import general packages
import os
import datetime
from ..smart_template.smart_template import SmartTemplate
from ..smart_template.hooks.code import wrap as hook_wrap, trim as hook_trim, indent as hook_indent

# Import SiLA2 library stuff
from ..fdl_parser.fdl_parser import FDLParser
from ..fdl_parser.type_base import DataType
from ..fdl_parser.type_basic import BasicType
from ..fdl_parser.type_list import ListType
from ..fdl_parser.type_constrained import ConstrainedType
from ..fdl_parser.type_structured import StructureType, StructureElementType
from ..fdl_parser.type_data_type_identifier import DataTypeIdentifier
from ..fdl_parser.command import Command
from ..fdl_parser.property import Property
from ..fdl_parser.metadata import Metadata
from ..fdl_parser.data_type_parameter import ParameterDataType
from ..fdl_parser.data_type_response import ResponseDataType
from ..fdl_parser.data_type_intermediate import IntermediateDataType

__VERSION__ = '0.2.0'

class ProtoBuilder:
    """gRPC protocol buffers file builder/compiler class"""

    #: Reference to the FDLParser object that is used as basis for the .proto files
    fdl_parser: FDLParser

    #: The namespace that is created by this package
    namespace_package: str

    #: The namespace used for standard SiLA defined messages in the .proto file
    namespace_sila: str = 'sila2.org.silastandard'

    def __init__(self, fdl_parser: FDLParser):
        """
        Class initialiser.

        :param fdl_parser: :class:`~..fdl_parser.fdl_parser.FDLParser` object (`from ..fdl_parser.fdl_parser
                           import FDLParser`).
        """

        # store basic inputs
        self.fdl_parser = fdl_parser

        # generate main namespace
        self.namespace_package = ".".join([
            "sila2",
            self.fdl_parser.originator,
            self.fdl_parser.category if self.fdl_parser.category is not None else 'none',
            self.fdl_parser.identifier.lower(),
            'v' + str(self.fdl_parser.feature_version_major)
        ])

    def write_proto(self, proto_dir: Union[str, None] = None, proto_filename: Union[str, None] = None) -> str:
        """
        Writes .proto to the proto_dir. Will generate all necessary data beforehand.

        :param proto_dir: The directory to which to write. If `None`, the same directory where the FDL file is stored
                          will be used.
        :param proto_filename: The filename of the proto file. if not given, the output file will have the same name as
                               the FDL/XML file with the .proto ending.

        :returns: The file name to which the proto code has been written.
        """

        if proto_filename is None:
            # generate the proto filename from the input filename of the fdl_parser
            proto_filename = str(os.path.basename(self.fdl_parser.fdl_filename).split(os.extsep)[0]) + '.proto'
            logging.info('Set output filename to "{proto_filename}"'.format(proto_filename=proto_filename))

        if proto_dir is None:
            proto_dir = os.path.dirname(self.fdl_parser.fdl_filename)
            logging.info('Automatically set directory for .proto files to "{proto_dir}"'.format(proto_dir=proto_dir))

        proto_output_file = os.path.join(proto_dir, proto_filename)
        proto_code = self._generate_proto()
        with open(proto_output_file, 'w', encoding='utf-8') as output_file:
            output_file.write(proto_code)

        return proto_output_file

    def _generate_proto(self) -> str:
        """
        Generate the .proto file content.

        :returns: Returns the code of the full .proto file.
        """

        # get the code for the separate parts
        proto_data_types = self._create_data_types()
        (service_commands, command_data_type_definitions) = self._create_commands()
        (service_properties, property_data_type_definitions) = self._create_properties()
        (service_metadata, metadata_data_type_definitions) = self._create_metadata()

        template = SmartTemplate(TEMPLATE_PROTO_FILE)
        template.add_function_hook('indent', hook_indent, [int])
        template.add_function_hook('comment', hook_comment, [str])
        template.add_function_hook('wrap', hook_wrap, [int])

        return template.substitute(
            package_namespace=self.namespace_package,
            feature_id=self.fdl_parser.identifier,
            feature_name=self.fdl_parser.name,
            feature_description=self.fdl_parser.description,
            service_commands=service_commands,
            service_properties=service_properties,
            service_metadata=service_metadata,
            data_type_definitions=proto_data_types,
            command_data_type_definitions=command_data_type_definitions,
            property_data_type_definitions=property_data_type_definitions,
            metadata_data_type_definitions=metadata_data_type_definitions,
            version=__VERSION__,
            generator=__name__,
            date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def _create_properties(self) -> (str, str):
        """
        Creating the properties part of the proto file.

        :returns: A tuple (code_rpc_calls, code_parameters) which contains the corresponding .proto code.
        """
        # pylint: disable=broad-except

        logging.debug("Creating properties for .proto files")

        # initialise local variables
        code_parameters = ""
        code_rpc_calls = ""

        for identifier, fdl_property in self.fdl_parser.properties.items():
            # initialise temporary variables, we only add commands when no error occurs anywhere
            temp_code_rpc_calls = ""
            temp_code_parameters = ""

            try:
                logging.debug('Found property: {property_id}'.format(property_id=identifier))

                temp_code_rpc_calls += self._generate_property_calls(fdl_property) + "\n"

                # Now let us create Parameters and Responses
                # Parameters
                temp_code_parameters += self._generate_command_arguments(
                    identifier=identifier,
                    prefix='Subscribe_' if fdl_property.observable else 'Get_',
                    postfix='_Parameters',
                    data_types={}
                ) + "\n"

                temp_code_parameters += self._generate_command_arguments(
                    identifier=identifier,
                    prefix='Subscribe_' if fdl_property.observable else 'Get_',
                    postfix='_Responses',
                    data_types={
                        fdl_property.response.identifier: fdl_property.response
                    }
                ) + "\n"

            except Exception as err:
                logging.exception(
                    "Failed to generate code for property {property}: {err}".format(
                        property=identifier,
                        err=err
                    )
                )
                continue

            code_parameters += temp_code_parameters
            code_rpc_calls += temp_code_rpc_calls

        return code_rpc_calls.strip(), code_parameters.strip()

    def _create_commands(self) -> (str, str):
        """
        Creating the commands part of the proto file.

        :returns: A tuple (code_rpc_calls, code_parameters) which contains the corresponding .proto code.
        """
        # pylint: disable=broad-except

        logging.debug("Creating commands for .proto file.")

        # initialise local variables
        code_parameters = ""
        code_rpc_calls = ""

        for identifier, command in self.fdl_parser.commands.items():
            # initialise temporary variables, we only add commands when no error occurs anywhere
            temp_code_rpc_calls = ""
            temp_code_parameters = ""

            try:
                logging.debug('Found command: {command_id}'.format(command_id=identifier))

                temp_code_rpc_calls += self._generate_command_calls(command) + "\n"

                # Now let us create Parameters and (intermediate) Responses
                # Parameters
                temp_code_parameters += self._generate_command_arguments(identifier=identifier,
                                                                         prefix='',
                                                                         postfix='_Parameters',
                                                                         data_types=command.parameters) + "\n"
                # Responses
                temp_code_parameters += self._generate_command_arguments(identifier=identifier,
                                                                         prefix='',
                                                                         postfix='_Responses',
                                                                         data_types=command.responses) + "\n"
                # Intermediate Responses
                if command.intermediates:
                    temp_code_parameters += self._generate_command_arguments(identifier=identifier,
                                                                             prefix='',
                                                                             postfix='_IntermediateResponses',
                                                                             data_types=command.intermediates) + "\n"

            except Exception as err:
                logging.exception(
                    "Failed to generate code for command {command}: {err}".format(
                        command=identifier,
                        err=err
                    )
                )
                continue

            code_parameters += temp_code_parameters
            code_rpc_calls += temp_code_rpc_calls

        return code_rpc_calls.strip(), code_parameters.strip()

    def _create_metadata(self) -> (str, str):
        """
        Create the metadata part of the proto file.

        :return: A tuple (code_rpc_calls, code_parameters) which contains the corresponding .proto code.
        """
        # pylint: disable=broad-except

        logging.debug("Creating metadata for .proto file.")

        # initialise local variables
        code_parameters = ""
        code_rpc_calls = ""

        for identifier, metadata in self.fdl_parser.metadata.items():
            # initialise temporary variables, we only add the code when no error occurs anywhere
            temp_code_rpc_calls = ""
            temp_code_parameters = ""

            try:
                logging.debug('Found metadata: {metadata_id}'.format(metadata_id=identifier))

                temp_code_rpc_calls += self._generate_metadata_calls(metadata) + "\n"

                temp_code_parameters += self._generate_metadata_messages(metadata) + "\n"

                temp_code_parameters += self._generate_command_arguments(
                    identifier=identifier,
                    prefix='Metadata_',
                    postfix='',
                    data_types={
                        metadata.parameter.identifier: metadata.parameter
                    }) + "\n"
            except Exception as err:
                logging.exception(
                    'Failed to generate code for metadata {metadata_id}: {err}'.format(
                        metadata_id=identifier,
                        err=err
                    )
                )
                continue

            code_parameters += temp_code_parameters
            code_rpc_calls += temp_code_rpc_calls

        return code_rpc_calls.strip(), code_parameters.strip()

    def _generate_property_calls(self, fdl_property: Property):
        # we need to distinguish between observable and not-observable properties
        if fdl_property.observable:
            rpc_template_string = TEMPLATE_RPC_PROPERTY_OBSERVABLE
        else:
            rpc_template_string = TEMPLATE_RPC_PROPERTY_UNOBSERVABLE

        template = SmartTemplate(template=rpc_template_string)
        return (
            ProtoBuilder._generate_description(fdl_property) + "\n" +
            template.substitute(
                property_id=fdl_property.identifier,
                package_namespace=self.namespace_package,
                sila_namespace=self.namespace_sila,
            )
        )

    def _generate_command_calls(self, command: Command):
        # we need to distinguish which kind of command we are talking about, and what responses are available
        if command.observable and command.intermediates:
            rpc_template_string = TEMPLATE_RPC_COMMAND_OBSERVABLE_INTERMEDIATE
        elif command.observable and not command.intermediates:
            rpc_template_string = TEMPLATE_RPC_COMMAND_OBSERVABLE_NO_INTERMEDIATE
        else:
            rpc_template_string = TEMPLATE_RPC_COMMAND_UNOBSERVABLE

        template = SmartTemplate(template=rpc_template_string)
        return (
            ProtoBuilder._generate_description(command) + "\n" +
            template.substitute(
                command_id=command.identifier,
                package_namespace=self.namespace_package,
                sila_namespace=self.namespace_sila,
            )
        )

    def _generate_metadata_calls(self, metadata: Metadata):
        rpc_template_string = TEMPLATE_RPC_METADATA

        template = SmartTemplate(template=rpc_template_string)
        return(
            ProtoBuilder._generate_description(metadata) + "\n" +
            template.substitute(
                metadata_id=metadata.identifier,
                package_namespace=self.namespace_package,
                sila_namespace=self.namespace_sila,
            )
        )

    def _generate_metadata_messages(self, metadata: Metadata):
        rpc_template_string = TEMPLATE_MESSAGE_METADATA

        template = SmartTemplate(template=rpc_template_string)
        return(
            template.substitute(
                metadata_id=metadata.identifier,
                package_namespace=self.namespace_package,
                sila_namespace=self.namespace_sila,
            )
        )

    def _generate_command_arguments(
            self,
            identifier: str,
            data_types: Dict[str, Union[ParameterDataType, ResponseDataType, IntermediateDataType]],
            prefix: str = '',
            postfix: str = '') -> str:

        # set general values and initialise variables
        prefix = prefix
        postfix = postfix
        definitions = []
        type_strings = []
        for index, argument_id in enumerate(data_types, 1):
            argument = data_types[argument_id]

            # get the substrings used
            namespace = self.namespace_package + "." + prefix + identifier + postfix
            (definition, type_string) = self._evaluate_data_type(data_type=argument.sub_type,
                                                                 identifier=argument.identifier,
                                                                 namespace=namespace)
            # allow parsing the substrings
            template = SmartTemplate(type_string)
            type_string = template.substitute(identifier=argument.identifier, index=index,
                                              namespace=self.namespace_package)

            if definition is not None:
                definitions.append(definition)
            type_strings.append(type_string)

        return (
            self._create_message_str(
                data_type=None,
                identifier=identifier,
                prefix=prefix,
                postfix=postfix,
                definitions=None if not definitions else definitions,
                type_strings=None if not type_strings else type_strings
            ) + "\n"
        )

    def _create_data_types(self) -> str:

        # prefix/postfix for this type
        prefix = "DataType_"
        postfix = ""

        # initialise the output variable
        code_content = ""

        for identifier, data_type in self.fdl_parser.data_type_definitions.items():
            # get the substrings used
            namespace = self.namespace_package + "." + prefix + identifier + postfix
            (definition, type_string) = self._evaluate_data_type(data_type=data_type.sub_type,
                                                                 identifier=data_type.identifier,
                                                                 namespace=namespace)
            # allow parsing the substrings
            if type_string is not None:
                template = SmartTemplate(type_string)
                type_string = template.substitute(identifier=identifier, index=1, namespace=self.namespace_package)
            # add the element to our code
            code_content += \
                self._create_message_str(
                    data_type=data_type,
                    identifier=identifier,
                    prefix=prefix,
                    postfix=postfix,
                    definitions=None if definition is None else [definition],
                    type_strings=None if type_string is None else [type_string]
                ) + "\n"

        return code_content.strip()

    def _evaluate_data_type(self, data_type: DataType, identifier: str, namespace: str) \
            -> (Union[str, None], Union[str, None]):

        if data_type.is_basic:
            return None, self._generate_basic_type_str(basic_type=data_type)
        elif data_type.is_list:
            return self._generate_list_type_str(list_type=data_type,
                                                identifier=identifier,
                                                namespace=namespace)
        elif data_type.is_constrained:
            return self._generate_constrained_type_str(constrained_type=data_type,
                                                       identifier=identifier,
                                                       namespace=namespace)
        elif data_type.is_structure:
            return self._generate_structure_type_str(structure_type=data_type,
                                                     identifier=identifier,
                                                     namespace=namespace)
        elif data_type.is_identifier:
            return None, self._generate_data_type_identifier_str(data_type_identifier_type=data_type)
        else:
            raise TypeError

    # pylint: disable=too-many-arguments
    def _create_message_str(self, data_type: Union[DataType, None], identifier: str, prefix: str = '',
                            postfix: str = '', definitions: List[str] = None, type_strings: List[str] = None) -> str:

        message_comment = ''
        if data_type is not None and data_type.is_sila_element:
            message_comment += self._generate_description(data_type=data_type)
            message_comment += "\n"

        message_contents = ''
        if definitions is not None:
            message_contents += '\n'.join(definitions)
            if type_strings is not None:
                message_contents += "\n"
        if type_strings is not None:
            message_contents += '\n'.join(type_strings)
        else:
            message_contents += "// Empty message"

        template = SmartTemplate(TEMPLATE_MESSAGE)
        template.add_function_hook('indent', hook_indent, [int])
        template.add_function_hook('trim', hook_trim, [ProtoBuilder._string_to_bool, ProtoBuilder._string_to_bool])

        mapping = {
            'identifier': identifier,
            'prefix': prefix,
            'postfix': postfix
        }

        return (
            message_comment +
            template.substitute(mapping=mapping, message=message_contents)
        )

    def _generate_basic_type_str(self, basic_type: Union[DataType, BasicType]) -> Union[str, None]:

        # Handle the special case of an empty data type
        if basic_type.sub_type == 'Void':
            return ''

        type_string = ".".join([self.namespace_sila, basic_type.sub_type])

        return type_string + " ${identifier} = ${index};"

    def _generate_list_type_str(self,
                                list_type: Union[DataType, ListType],
                                identifier: str,
                                namespace: str) -> (Union[str, None], Union[str, None]):

        (definition, type_string) = self._evaluate_data_type(data_type=list_type.sub_type,
                                                             identifier=identifier,
                                                             namespace=namespace)

        if type_string is not None:
            type_string = "repeated " + type_string

        return definition, type_string

    def _generate_constrained_type_str(self,
                                       constrained_type: Union[DataType, ConstrainedType],
                                       identifier: str,
                                       namespace: str) -> (Union[str, None], Union[str, None]):
        (definition, type_string) = self._evaluate_data_type(data_type=constrained_type.sub_type,
                                                             identifier=identifier,
                                                             namespace=namespace)
        if type_string is not None:
            type_string = '// Constrained type, not reflected in protocol buffers' + '\n' + type_string

        return definition, type_string

    def _generate_structure_type_str(self,
                                     structure_type: Union[DataType, StructureType],
                                     identifier: str,
                                     namespace: str) -> (Union[str, None], Union[str, None]):

        # initialise local variables
        definitions = []
        type_strings = []

        struct_identifier = identifier + '_Struct'
        struct_namespace = '.'.join([namespace, struct_identifier])

        # noinspection PyUnusedLocal
        structure_element: StructureElementType
        for index, structure_element in enumerate(structure_type.sub_type, 1):
            # get the substrings used
            (definition, type_string) = self._evaluate_data_type(
                data_type=structure_element.sub_type,
                identifier=structure_element.identifier,
                namespace=struct_namespace)
            # allow parsing the substrings
            if type_string is not None:
                template = SmartTemplate(type_string)
                type_string = \
                    ProtoBuilder._generate_description(structure_element) + "\n" + \
                    template.substitute(identifier=structure_element.identifier,
                                        index=index,
                                        namespace=namespace)

            if definition is not None:
                definitions.append(definition)
            type_strings.append(type_string)

        # generate the definition of the struct
        definition = self._create_message_str(
            data_type=structure_type,
            identifier=struct_identifier,
            prefix='',
            postfix='',
            definitions=None if not definitions else definitions,
            type_strings=None if not type_strings else type_strings
        )

        # generate the type string of the struct
        type_string = struct_namespace + " ${identifier} = ${index};"

        return definition, type_string

    @staticmethod
    def _generate_data_type_identifier_str(data_type_identifier_type: Union[DataType, DataTypeIdentifier]) \
            -> Union[str, None]:

        # type_string = ".".join([namespace, data_type_identifier_type.sub_type])
        return "${namespace}.DataType_" + data_type_identifier_type.sub_type + " ${identifier} = ${index};"

    @staticmethod
    def _generate_description(data_type: Union[DataType, Command, Property, Metadata]) -> str:

        template = SmartTemplate(TEMPLATE_DESCRIPTION)
        template.add_function_hook('wrap', hook_wrap, [int])
        template.add_function_hook('comment', hook_comment, [str])

        mapping = {
            'display_name': data_type.name,
            'identifier': data_type.identifier,
            'description': data_type.description
        }

        return template.substitute(mapping=mapping)

    @staticmethod
    def _string_to_bool(input_string: str) -> bool:
        """
        Convert a string to a boolean while evaluating the strings contents.
            This function will convert the input string into a boolean value, while evaluating the contents of the
            string. Thus it will do the following checks:

            * If the `input_string` is 'False' or '0', it will return `False`.
            * Otherwise it will return bool(input_string), which can still return `False` if e.g. the string is empty.

        :param input_string: The string to evaluate.

        :returns: The boolean value of the string.
        """
        if input_string.lower() == 'false' or input_string == '0':
            return False
        else:
            return bool(input_string)


TEMPLATE_DESCRIPTION = """
// ${display_name}
${comment(//   ):wrap(120):description}
""".strip()

TEMPLATE_MESSAGE = """
message ${prefix}${identifier}${postfix} {
${indent(4):message}
}
""".strip()

TEMPLATE_RPC_COMMAND_UNOBSERVABLE = """
rpc ${command_id}(${package_namespace}.${command_id}_Parameters) returns (${package_namespace}.${command_id}_Responses) {}
""".strip()

TEMPLATE_RPC_COMMAND_OBSERVABLE_INTERMEDIATE = """
rpc ${command_id}(${package_namespace}.${command_id}_Parameters) returns (${sila_namespace}.CommandConfirmation) {}
rpc ${command_id}_Intermediate(${sila_namespace}.CommandExecutionUUID) returns (stream ${package_namespace}.${command_id}_IntermediateResponses) {}
rpc ${command_id}_Info(${sila_namespace}.CommandExecutionUUID) returns (stream ${sila_namespace}.ExecutionInfo) {}
rpc ${command_id}_Result(${sila_namespace}.CommandExecutionUUID) returns (${package_namespace}.${command_id}_Responses) {}
""".strip()

TEMPLATE_RPC_COMMAND_OBSERVABLE_NO_INTERMEDIATE = """
rpc ${command_id}(${package_namespace}.${command_id}_Parameters) returns (${sila_namespace}.CommandConfirmation) {}
rpc ${command_id}_Info(${sila_namespace}.CommandExecutionUUID) returns (stream ${sila_namespace}.ExecutionInfo) {}
rpc ${command_id}_Result(${sila_namespace}.CommandExecutionUUID) returns (${package_namespace}.${command_id}_Responses) {}
""".strip()

TEMPLATE_RPC_PROPERTY_UNOBSERVABLE = """
rpc Get_${property_id}(${package_namespace}.Get_${property_id}_Parameters) returns (${package_namespace}.Get_${property_id}_Responses) {}
""".strip()

TEMPLATE_RPC_PROPERTY_OBSERVABLE = """
rpc Subscribe_${property_id}(${package_namespace}.Subscribe_${property_id}_Parameters) returns (stream ${package_namespace}.Subscribe_${property_id}_Responses) {}
""".strip()

TEMPLATE_RPC_METADATA = """
rpc Get_FCPAffectedByMetadata_${metadata_id}(${package_namespace}.Get_FCPAffectedByMetadata_${metadata_id}_Parameters) returns (${package_namespace}.Get_FCPAffectedByMetadata_${metadata_id}_Responses) {}
""".strip()

TEMPLATE_MESSAGE_METADATA = """
message Get_FCPAffectedByMetadata_${metadata_id}_Parameters {}
message Get_FCPAffectedByMetadata_${metadata_id}_Responses {
    repeated ${sila_namespace}.String AffectedCalls = 1;
}
""".strip()

TEMPLATE_PROTO_FILE = """
// This file is automatically generated by ${generator} version ${version}
// :generation date: ${date}
//
// ---- PLEASE DO NOT MODIFY MANUALLY !! ---

syntax = "proto3";
import "SiLAFramework.proto";
package ${package_namespace};

// Feature: ${feature_name}
${comment(//   ):wrap(120):feature_description}
service ${feature_id} {
${indent(4):service_commands}
${indent(4):service_properties}
${indent(4):service_metadata}
}

// ----------------- Data Type definitions -----------------
${data_type_definitions}

// ------ Command Parameter and Response definitions -------
${command_data_type_definitions}
${property_data_type_definitions}

// ----------------- Metadata Definitions ------------------
${metadata_data_type_definitions}
""".strip()


# defined here als long as smart_template hook is not in master
# TODO: Remove when implemented there
def hook_comment(input_string: str, comment_char: str = '# ') -> str:
    r"""
    Comment the given string

        :param input_string: The string to comment. Multi-line strings will receive a comment on each line
        :param comment_char: The character(s) to add at the beginning of each line

        :return: The commented string

        .. note:: Block-comments are not supported at the moment
    """
    return (
        comment_char +
        input_string.replace('\n', "\n" + comment_char)
    )
