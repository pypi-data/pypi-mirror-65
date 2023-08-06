"""
________________________________________________________________________

:PROJECT: SiLA2_python

* sila_server *

:details: Basic SiLA2 server.

:file:    sila_server.py
:authors: Mark Doerr
          Timm Severin

:date: (creation)          2018-11-28
:date: (last modification) 2019-08-27

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.2.0"

import os

import time
import logging
from configparser import ConfigParser
from typing import Optional, Dict, Any

import grpc
from grpc import server as grpc_server
from concurrent.futures import ThreadPoolExecutor

# Import the basic standard features that a SiLA Server *must* or should implement
#   SiLAService: Required, provides basic functionality for a SiLA server
from .framework.std_features import SiLAService as SiLAService_feature
from .framework.std_features import SiLAService_pb2_grpc as SiLAService_feature_grpc
#   SimulationController, allows to switch between simulation and real mode
from .framework.std_features import SimulationController as SimController_feature
from .framework.std_features import SimulationController_pb2_grpc as SimController_feature_grpc

from .sila_service_detection import SiLA2ServiceDetection
from ._internal.config import read_config_file


class SiLA2Server:
    """Base class of a SiLA2 Server"""
    #: A dictionary of all servicers of the features added to the server
    registered_servicers: Dict[str, Any]

    #: The grpc server object
    grpc_server: grpc.Server

    #: Port number under which the server is available
    server_port: int

    #: IP address of the server
    server_ip: str

    #: Storage for the ConfigParser object that allows to access the configuration
    sila2_config: ConfigParser

    #: Encryption mode of the server active or not
    encryption: bool

    #: The server certificate
    server_cert: bytes

    #: The server key
    server_key: bytes

    #: Storage for the SimulationController object that takes care of the simulation mode of the server
    SimulationController_feature: SimController_feature

    #: Storage for the SiLAService object that takes care of storing some basic server properties
    SiLAService_feature: SiLAService_feature

    def __init__(self,
                 name: str, description: str = "",
                 server_type: str = "", server_uuid: Optional[str] = None,
                 version: str = "0.0",
                 vendor_url: str = "",
                 ip: str = '127.0.0.1', port: int = 50051,
                 key_file: Optional[str] = 'sila_server.key', cert_file: Optional[str] = 'sila_server.crt',
                 simulation_mode: bool = True):
        """
        Initialising and starting the gRPC server, which is the core of the SiLA server.

        :param name: Name of the server
        :param description: Description of the Server
        :param server_type: The type of the server
        :param server_uuid: The UUID of the server. If not set, it will be generated/read automatically from the
                            configuration. If given, it will *not* be written automatically to the configuration file.
        :param version: Version of this server software
        :param vendor_url: Vendor URL of the Server
        :param ip: Server IP address
        :param port: Server port number
        :param key_file: Filename of private server key
        :param cert_file: Filename of server certificate
        """

        # read default values from config file
        self.sila2_config = read_config_file('server', name)

        # Generate sub-classes that take care of some data
        #   SiLAService
        self.SiLAService_feature = SiLAService_feature.SiLAService(
            server_name=name,
            server_description=description,
            server_version=version,
            server_type=server_type,
            server_UUID=server_uuid if server_uuid is not None else self.sila2_config['server']['UUID'],
            vendor_URL=vendor_url
        )

        #   Simulation controller
        self.SimulationController_feature = SimController_feature.SimulationController(
            sila2_server=self,
            simulation_mode=simulation_mode
        )

        # Networking
        self.server_ip = ip
        self.server_port = port

        # Encryption
        if key_file is None or cert_file is None:
            logging.info('Starting server without any encryption.')
            self.encryption = False
        else:
            try:
                with open(key_file, 'rb') as file:
                    self.server_key = file.read()
                with open(cert_file, 'rb') as file:
                    self.server_cert = file.read()
                self.encryption = True
            except FileNotFoundError as err:
                logging.error(
                    (
                        'Could not access files for encryption, '
                        'no encryption will be used: {err}'
                    ).format(err=err))
                self.encryption = False

        # Create the grpc-server
        self.grpc_server = grpc_server(ThreadPoolExecutor(max_workers=10))

        if self.encryption:
            server_credentials = grpc.ssl_server_credentials(
                private_key_certificate_chain_pairs=(self.server_key, self.server_cert)
            )

            self.grpc_server.add_secure_port('[::]:{port}'.format(port=self.server_port), server_credentials)
        else:
            self.grpc_server.add_insecure_port('[::]:{port}'.format(port=self.server_port))

        # Activate the standard features
        #   SiLAService
        SiLAService_feature_grpc.add_SiLAServiceServicer_to_server(self.SiLAService_feature, self.grpc_server)
        # SimulationController
        SimController_feature_grpc.add_SimulationControllerServicer_to_server(
            self.SimulationController_feature, self.grpc_server
        )
        self.add_feature(
            feature_id="SimulationController",
            servicer=None,
            data_path=os.path.join(
                os.path.dirname(__file__), #path to sila2lib
                'framework',
                'feature_definitions',
                'org.silastandard'
            )
        )

        # prepare storage to access all servicers
        self.registered_servicers = {}

    def add_feature(self, feature_id: str, servicer, data_path: str) -> None:
        """
        Adds a feature to this server.

        :param feature_id: The feature id of the feature to add to this server
        :param servicer: The servicer for the corresponding feature. This is automatically used to allow access to it
                         and to set the simulation/real mode. If This is not available, None can be passed and the
                         feature will not be stored in this class. It will, however, still be registered in the
                         SiLAService module.
        :param data_path: Path where the FDL data is stored. FDL data must be supplied as *.sila.xml file. The filename
                          is expected to be <FeatureId>.<ending>.
        """
        # determine suggestions for the input data paths
        #   XML
        xml_file = os.path.join(data_path, '{feature_id}.sila.xml'.format(feature_id=feature_id))
        if not os.path.exists(xml_file):
            xml_file = None

        # register the feature
        self.SiLAService_feature.registerFeature(
            feature_id=feature_id,
            xml_fdl=xml_file,
        )

        if servicer is not None:
            self.registered_servicers[feature_id] = servicer

    @property
    def simulation_mode(self):
        return self.SimulationController_feature.simulation_mode

    @simulation_mode.setter
    def simulation_mode(self, value: bool):
        if value:
            self.SimulationController_feature.StartSimulationMode(request=None, context=None)
        else:
            self.SimulationController_feature.StartRealMode(request=None, context=None)

    @property
    def server_name(self):
        return self.SiLAService_feature.server_name

    @property
    def server_description(self):
        return self.SiLAService_feature.server_description

    @property
    def server_version(self):
        return self.SiLAService_feature.server_version

    @property
    def server_uuid(self):
        return self.SiLAService_feature.server_UUID

    def run(self, block: bool = True) -> None:
        """
        Main gRPC server routine

        :param block: If set to True, this function will block the execution of the main thread until CTRL-C is pressed
                      to shutdown the gRPC server. Otherwise this function won't block the main thread and return
                      immediately. Note that you are then responsible to shutdown the gRPC server yourself by calling
                      `~stop_grpc_server()`.
        """
        self.grpc_server.start()

        # enabling zeroconf/Bonjour Service detection
        service_detection = SiLA2ServiceDetection()
        service_detection.registerService(
            service_name=self.SiLAService_feature.server_name,
            IP=self.server_ip,
            port=self.server_port,
            server_uuid=self.SiLAService_feature.server_UUID
        )

        print("Server '{server_name}' started!".format(server_name=self.SiLAService_feature.server_name))
        if block:
            print("Please press ctrl-c to stop...")
            try:
                while True:
                    time.sleep(60*60*24)
            except KeyboardInterrupt:
                self.grpc_server.stop(0)

    def stop_grpc_server(self, force: bool = False) -> None:
        """
        Immediately stops the grpc server.

        :param force: If set to True, immediately stop the server no matter what. Otherwise try to finish all ongoing
                      processes first.

        .. note:: When implementing this routine, remember to terminate all observable commands and properties if no
                  forced stop is requested.
        """

        if not force:
            # Terminate ongoing processes, allow submodules to finish
            pass

        logging.info("Stopping server '{server_name}'".format(server_name=self.SiLAService_feature.server_name))
        self.grpc_server.stop(0)

    def _switch_to_simulation_mode(self) -> None:
        """Switching to simulation mode."""
        for feature_id in self.registered_servicers:
            try:
                self.registered_servicers[feature_id].switch_to_simulation_mode()
            except AttributeError:
                logging.error(
                    'Could not automatically set feature {feature_id} to simulation mode, '
                    'feature does not implement the switch_to_simulation_mode() method.'.format(
                        feature_id=feature_id
                    )
                )

    def _switch_to_real_mode(self) -> None:
        """Switching to real mode."""
        for feature_id in self.registered_servicers:
            try:
                self.registered_servicers[feature_id].switch_to_real_mode()
            except AttributeError:
                logging.error(
                    'Could not automatically set feature {feature_id} to real mode, '
                    'feature does not implement the switch_to_real_mode() method.'.format(
                        feature_id=feature_id
                    )
                )

    def toggleSimMode(self):
        """Toggle between simulation and real mode."""
        logging.debug('Toggle of simulation/real mode requested:')
        self.simulation_mode = not self.simulation_mode

    def rename_server(self, new_server_name: str):
        """
        Change the name of the server.

        :param new_server_name: New server name.
        """

        logging.debug("Renaming SiLA server from [{old_name}] to [{new_name}]".format(
            old_name=self.SiLAService_feature.server_name,
            new_name=new_server_name
        ))

        self.SiLAService_feature.server_name = new_server_name
