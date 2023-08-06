
from typing import Dict

from ..fdl_parser.fdl_parser import FDLParser
from ..proto_builder.proto_builder import ProtoBuilder
from ..proto_builder.proto_compiler import compile_proto_to_python

from ._dynamic_command import _DynamicCommand
from ._dynamic_property import _DynamicProperty

import os
import sys
import grpc
import importlib


class DynamicFeature:

    # the feature this handler is defined for
    feature_id: str

    #: The path on which this handler operates, i.e. where all files are stored/read from
    storage_path: str

    # Storage objects for access to the feature
    #: Commands that are stored in the feature
    commands: Dict[str, _DynamicCommand]
    #: Properties that are stored in this feature
    properties: Dict[str, _DynamicProperty]

    # The modules generated for this feature
    #: The grpc module for all access commands
    _module_pb2_grpc: object
    #: The protobuf module defining the parameters and expected responses
    _module_pb2: object

    def __init__(self, fdl_file: str, channel: grpc.Channel):

        self.storage_path = os.path.dirname(fdl_file)

        # read the FDL file
        fdl_parser = FDLParser(fdl_filename=fdl_file)
        self.feature_id = fdl_parser.identifier

        # generate a proto file from it
        proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
        proto_file = proto_builder.write_proto(self.storage_path)

        # compile the proto file
        result = compile_proto_to_python(
            proto_file=os.path.basename(proto_file),
            source_dir=self.storage_path,
            target_dir=self.storage_path
        )
        if not result:
            raise RuntimeError('Could not compile proto file "{file}"'.format(file=proto_file))

        # to easily load the modules we add their directory to the path.
        #   Theoretically there should be other ways to load the modules, however they did not work for me.
        #   Tried: importlib.utils.spec_from_file_location / importlib.utils.module_from_spec
        if self.storage_path not in sys.path:
            sys.path.append(self.storage_path)

        self._module_pb2 = importlib.import_module(
            '{feature}_pb2'.format(feature=os.path.splitext(os.path.basename(proto_file))[0]))
        self._module_pb2_grpc = importlib.import_module(
            '{feature}_pb2_grpc'.format(feature=os.path.splitext(os.path.basename(proto_file))[0]))

        # load access to all defined commands and properties
        feature_stub_class = getattr(self._module_pb2_grpc, '{feature}Stub'.format(feature=self.feature_id))
        feature_stub = feature_stub_class(channel)
        self.commands = {}
        for command_id in fdl_parser.commands:
            self.commands[command_id] = _DynamicCommand(command=fdl_parser.commands[command_id],
                                                        fdl_parser=fdl_parser,
                                                        feature_stub=feature_stub,
                                                        feature_pb2=self._module_pb2)

        self.properties = {}
        for property_id in fdl_parser.properties:
            self.properties[property_id] = _DynamicProperty(property_element=fdl_parser.properties[property_id],
                                                            fdl_parser=fdl_parser,
                                                            feature_stub=feature_stub,
                                                            feature_pb2=self._module_pb2)
