
import grpc

from . import SiLAService_pb2


class SiLAServiceStub:

    def __init__(self, channel: grpc.Channel) -> None:
        pass

    def GetFeatureDefinition(self, parameters: SiLAService_pb2.GetFeatureDefinition_Parameters) \
            -> SiLAService_pb2.GetFeatureDefinition_Responses:
        pass

    def SetServerName(self, parameters: SiLAService_pb2.SetServerName_Parameters) \
            -> SiLAService_pb2.SetServerName_Responses:
        pass

    def Get_ServerName(self, parameters: SiLAService_pb2.Get_ServerName_Parameters) \
            -> SiLAService_pb2.Get_ServerName_Responses:
        pass

    def Get_ServerType(self, parameters: SiLAService_pb2.Get_ServerType_Parameters) \
            -> SiLAService_pb2.Get_ServerType_Responses:
        pass

    def Get_ServerUUID(self, parameters: SiLAService_pb2.Get_ServerUUID_Parameters) \
            -> SiLAService_pb2.Get_ServerUUID_Responses:
        pass

    def Get_ServerDescription(self, parameters: SiLAService_pb2.Get_ServerDescription_Parameters) \
            -> SiLAService_pb2.Get_ServerDescription_Responses:
        pass

    def Get_ServerVersion(self, parameters: SiLAService_pb2.Get_ServerVersion_Parameters) \
            -> SiLAService_pb2.Get_ServerVersion_Responses:
        pass

    def Get_ServerVendorURL(self, parameters: SiLAService_pb2.Get_ServerVendorURL_Parameters) \
            -> SiLAService_pb2.Get_ServerVendorURL_Responses:
        pass

    def Get_ImplementedFeatures(self, parameters: SiLAService_pb2.Get_ImplementedFeatures_Parameters) \
            -> SiLAService_pb2.Get_ImplementedFeatures_Responses:
        pass


class SiLAServiceServicer(object):

    def GetFeatureDefinition(self,
                             request: SiLAService_pb2.GetFeatureDefinition_Parameters,
                             context: grpc.ServicerContext) \
            -> SiLAService_pb2.GetFeatureDefinition_Responses:
        pass

    def SetServerName(self,
                      request: SiLAService_pb2.SetServerName_Parameters,
                      context: grpc.ServicerContext) \
            -> SiLAService_pb2.SetServerName_Responses:
        pass

    def Get_ServerName(self,
                       request: SiLAService_pb2.Get_ServerName_Parameters,
                       context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerName_Responses:
        pass

    def Get_ServerType(self,
                         request: SiLAService_pb2.Get_ServerType_Parameters,
                       context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerName_Responses:
        pass

    def Get_ServerUUID(self,
                       request: SiLAService_pb2.Get_ServerUUID_Parameters,
                       context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerUUID_Responses:
        pass

    def Get_ServerDescription(self,
                              request: SiLAService_pb2.Get_ServerDescription_Parameters,
                              context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerDescription_Responses:
        pass

    def Get_ServerVersion(self,
                          request: SiLAService_pb2.Get_ServerVersion_Parameters,
                          context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerVersion_Responses:
        pass

    def Get_ServerVendorURL(self,
                            request: SiLAService_pb2.Get_ServerVendorURL_Parameters,
                            context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ServerVendorURL_Responses:
        pass

    def Get_ImplementedFeatures(self,
                                request: SiLAService_pb2.Get_ImplementedFeatures_Parameters,
                                context: grpc.ServicerContext) \
            -> SiLAService_pb2.Get_ImplementedFeatures_Responses:
        pass

def add_SiLAServiceServicer_to_server(servicer, server) -> None:
    pass