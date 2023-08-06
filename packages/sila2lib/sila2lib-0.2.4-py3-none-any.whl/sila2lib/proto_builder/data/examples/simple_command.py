
import sys
import os
import importlib

from sila2lib.fdl_parser.fdl_parser import FDLParser
from sila2lib.proto_builder.proto_builder import ProtoBuilder
from sila2lib.proto_builder.proto_compiler import compile_proto_to_python

from sila2lib.proto_builder.data.data_parameters import DataParameters

# ---------------------------------------
#   Config
# ---------------------------------------

fdl_input = 'SimpleCommand.sila.xml'

output_dir = './SimpleCommand'

command_id = 'MakeCoffee'

# ---------------------------------------
#   Preparation
# ---------------------------------------

output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)

# read the FDL file
fdl_parser = FDLParser(fdl_filename=fdl_input)
feature_id = fdl_parser.identifier

# generate a proto file from it
proto_builder = ProtoBuilder(fdl_parser=fdl_parser)
proto_file = proto_builder.write_proto(proto_dir=output_dir)

# compile the proto file
result = compile_proto_to_python(
    proto_file=os.path.basename(proto_file),
    source_dir=output_dir,
    target_dir=output_dir
)
if not result:
    raise RuntimeError('Could not compile proto file "{file}"'.format(file=proto_file))

# to easily load the modules we add their directory to the path.
#   Theoretically there should be other ways to load the modules, however they did not work for me.
#   Tried: importlib.utils.spec_from_file_location / importlib.utils.module_from_spec
if output_dir not in sys.path:
    sys.path.append(output_dir)

module_pb2 = importlib.import_module('{feature}_pb2'.format(feature=os.path.splitext(os.path.basename(proto_file))[0]))

test_obj = DataParameters(identifier=command_id, content=list(fdl_parser.commands[command_id].parameters.values()), feature_pb2=module_pb2, fdl_parser=fdl_parser)
print(test_obj)
