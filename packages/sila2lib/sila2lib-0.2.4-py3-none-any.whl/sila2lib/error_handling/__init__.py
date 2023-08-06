
# ----------------------------------------------------------------------
# (Sub-)Package wide configuration options
# ----------------------------------------------------------------------

# Serialise the error message via the gRPC/protobuf default                     False
#   protobuf.Message.SerializeToString()
# or use an additional base64 encoding as defined in the SiLA standard          True
#   base64.b64encode(msg.encode('utf-8'))
use_base64_encoding = True
