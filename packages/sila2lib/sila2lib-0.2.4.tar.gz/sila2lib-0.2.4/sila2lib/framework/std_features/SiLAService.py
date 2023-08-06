"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLAService standard feature*

:details: The Feature each SiLA Server MUST implement. It is the entry point to a SiLA Server and helps to discover
          the features it implements.

:file:    SiLAService.py
:authors: Mark Doerr
          Timm Severin

:date: (creation)          2019-02-02
:date: (last modification) 2019-08-26

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
from typing import Dict, Any

__version__ = "0.2.0"

import os
import logging
import grpc

# importing protobuf and gRPC handler/stubs
from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2
from sila2lib.error_handling.server_err import SiLAValidationError

from . import SiLAService_pb2 as pb2
from . import SiLAService_pb2_grpc as pb2_grpc


# noinspection PyPep8Naming
class SiLAService(pb2_grpc.SiLAServiceServicer):
    """
    The Feature each SiLA Server MUST implement. It is the entry point to a SiLA Server and helps to discover the
    features it implements.
    """
    #: The name of the server
    server_name: str

    #: Description of the server
    server_description: str

    #: Software version of the server
    server_version: str

    # Type of the server
    server_type: str

    #: The UUID of the server
    server_UUID: str

    # The vendors URL
    vendor_URL: str

    #: Dictionary of implemented features that are registered to the SiLAService provider
    implemented_features: Dict[str, str]

    def __init__(self, server_name: str, server_description: str, server_version: str,
                 server_type: str, server_UUID: str, vendor_URL: str):
        """SiLAService class initialiser"""

        logging.debug("Initialising org.silastandard feature: SiLAService")

        # Initialise class variables
        self.implemented_features = {}

        # Store the inputs
        self.server_name = server_name
        self.server_description = server_description
        self.server_version = server_version
        self.server_type = server_type
        self.server_UUID = server_UUID
        self.vendor_URL = vendor_URL

        # read the feature definition (FDL) from the library
        sila_service_fdl = os.path.join(os.path.dirname(__file__), '..', 'feature_definitions','org.silastandard', 'SiLAService.sila.xml')
        self.registerFeature('SiLAService', sila_service_fdl)

    def GetFeatureDefinition(self, request, context: grpc.ServicerContext) -> pb2.GetFeatureDefinition_Responses:
        """
        Get all details on one Feature through the qualified Feature id.

        :param request: gRPC request
            request.QualifiedFeatureIdentifier: The qualified Feature identifier for which the Feature description
                                                should be retrieved.
        :param context: gRPC context.
        """
        feature_id = request.QualifiedFeatureIdentifier.value

        logging.debug('Feature definition for feature {feature_id} requested.'.format(feature_id=feature_id))

        try:
            return pb2.GetFeatureDefinition_Responses(
                FeatureDefinition=silaFW_pb2.String(value=self.implemented_features[feature_id])
            )
        except KeyError:
            logging.error('Feature {feature_id} not registered.'.format(feature_id=feature_id))
            err = SiLAValidationError(parameter="QualifiedFeatureIdentifier.Identifier",
                                      msg='Feature {feature_id} is unknown.'.format(feature_id=feature_id))
            err.raise_rpc_error(context=context)

    def SetServerName(self, request, context: grpc.ServicerContext) -> pb2.SetServerName_Responses:
        """
        Sets a human readable name to the Server Name property.

        :param request: gRPC request
            request.ServerName: The human readable name of to assign to the SiLA Server.
        :param context: gRPC context.
        """
        self.server_name = request.ServerName.value

        logging.debug("Server name changed to {server_name}".format(server_name=self.server_name))

        return pb2.SetServerName_Responses()

    def Get_ServerName(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerName_Responses:
        """
        Human readable name of the SiLA Server.

        :param request: gRPC request.
        :param context: gRPC context.

        :returns:
            response.ServerName: Human readable name of the SiLA Server.
        """
        logging.debug("Get_ServerName: {server_name}".format(server_name=self.server_name))

        return pb2.Get_ServerName_Responses(ServerName=silaFW_pb2.String(value=self.server_name))

    def Get_ServerType(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerType_Responses:
        """
        The type of Server this is. Is specified by the implementer of the server and not unique.

        :param request: gRPC request.
        :param context: gRPC context.

        :returns:
            response.ServerType: The type of Server this is. Is specified by the implementer of the server and not
                                 unique.
        """
        logging.debug("Get_ServerType: {}".format(self.server_type))

        return pb2.Get_ServerType_Responses(ServerType=silaFW_pb2.String(value=self.server_type))

    def Get_ServerUUID(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerUUID_Responses:
        """
        Globally unique identifier that identifies a SiLA Server. The Server UUID *must* be generated once and always
        remain the same.

        :param request: gRPC request.
        :param context: gRPC context.

        :returns:
            response.ServerUUID: Globally unique identifier that identifies a SiLA Server. The Server UUID *must* be
                                 generated once and always remain the same.
        """
        logging.debug("Get_ServerUUID: {server_uuid}".format(server_uuid=self.server_UUID))

        return pb2.Get_ServerUUID_Responses(ServerUUID=silaFW_pb2.String(value=self.server_UUID))

    def Get_ServerDescription(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerDescription_Responses:
        """
        Description of the SiLA Server.

        :param request: gRPC request.
        :param context: gRPC context.

        :returns:
            response.ServerDescription: Description of the SiLA Server.
        """
        logging.debug("Get_ServerDescription: {server_description}".format(server_description=self.server_description))

        return pb2.Get_ServerDescription_Responses(ServerDescription=silaFW_pb2.String(value=self.server_description))

    def Get_ServerVersion(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerVersion_Responses:
        """
        Returns the version of the SiLA Server. A "Major" and a "Minor" version number (e.g. 1.0) *must* be provided, a
        Patch version number _may_ be provided. Optionally, an arbitrary text, separated by an underscore _may_ be
        appended, e.g. “3.19.373_mighty_lab_devices”.

        :param request: gRPC request
        :param context: gRPC context

        :returns:
            response.ServerVersion: Returns the version of the SiLA Server. A "Major" and a "Minor" version number
                                    (e.g. 1.0) *must* be provided, a Patch version number _may_ be provided. Optionally,
                                    an arbitrary text, separated by an underscore _may_ be appended, e.g.
                                    “3.19.373_mighty_lab_devices”.
        """
        logging.debug("Get_ServerVersion: {server_version}".format(server_version=self.server_version))

        return pb2.Get_ServerVersion_Responses(ServerVersion=silaFW_pb2.String(value=self.server_version))

    def Get_ServerVendorURL(self, request, context: grpc.ServicerContext) -> pb2.Get_ServerVendorURL_Responses:
        """
        Returns the URL to the website of the vendor or the website of the product of this SiLA Server.

        :param request: gRPC request.
        :param context: gRPC context.

        :returns:
            response.ServerVendorURL: Returns the URL to the website of the vendor or the website of the product of
                                      this SiLA Server.
        """
        logging.debug("Get_ServerVendorURL: {vendor_url}".format(vendor_url=self.vendor_URL))

        return pb2.Get_ServerVendorURL_Responses(
            ServerVendorURL=silaFW_pb2.String(value=self.vendor_URL)
        )

    def Get_ImplementedFeatures(self, request, context: grpc.ServicerContext) -> pb2.Get_ImplementedFeatures_Responses:
        """
        Returns a list of qualified Feature identifiers of all implemented Features of this SiLA Server.

        :param request: gRPC request
        :param context: gRPC context

        :returns:
            response.ImplementedFeatures: Returns a list of qualified Feature identifiers of all implemented Features
                                          of this SiLA Server.
        """

        logging.debug("Get_ImplementedFeatures {feature_list}".format(
            feature_list=', '.join(self.implemented_features.keys()))
        )

        feature_list = [
            silaFW_pb2.String(value=feature_id)
            for feature_id in
            self.implemented_features
        ]

        return pb2.Get_ImplementedFeatures_Responses(
            ImplementedFeatures=feature_list
        )

    def registerFeature(self, feature_id: str, xml_fdl: str = None) -> None:
        """
        Registers a new feature to the server so its FeatureDefinition can be provided to the client.

        :param feature_id: Feature identifier to add.
        :param xml_fdl: The feature definition file of the feature to register in XML format.
        """

        if xml_fdl is not None:
            with open(xml_fdl, 'r', encoding='utf-8') as file:
                fdl = file.read()
        else:
            # no FDL input given
            logging.error('For feature {feature_id} no FDL data has been provided!'.format(feature_id=feature_id))
            fdl = '<xml>Feature Definition Missing for this feature.</xml>'

        # compressing the FDL, by removing \n and \r
        self.implemented_features[feature_id] = fdl.replace('\n', ' ').replace('\r', '')
