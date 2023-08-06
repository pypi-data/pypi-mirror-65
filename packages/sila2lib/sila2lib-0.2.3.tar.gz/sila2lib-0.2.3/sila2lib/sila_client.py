"""
________________________________________________________________________

:PROJECT: SiLA2_python

* sila_client *

:details: Basic SiLA2 client.

:file:    sila_client.py
:authors: Mark Doerr
          Timm Severin

:date: (creation)          2019-01-05
:date: (last modification) 2019-08-27

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
from configparser import ConfigParser

__version__ = "0.2.0"

# import general packages required
import logging
import grpc

from typing import Optional, Union

from abc import ABC, abstractmethod

# import SiLA2 library packages
from .framework.std_features import SiLAService_pb2_grpc as SiLAService_feature_grpc
from .framework.std_features import SimulationController_pb2 as SimController_feature_pb2
from .framework.std_features import SimulationController_pb2_grpc as SimController_feature_grpc

from ._internal.config import read_config_file


class SiLA2Client(ABC):
    """
    Base class for a SiLA2 client
    """

    #: Access to the SimulationController stubs to control the simulation/real mode behaviour of the server
    SimulationController_stub: SimController_feature_grpc

    #: Access to the SiLAService stubs to obtain primary server information
    SiLAService_stub: SiLAService_feature_grpc

    #: Store the grpc channel which is used to communicate with the server
    channel: grpc.Channel

    #: Store whether encryption is used in the connection
    encryption: bool

    #: The server certificate which is used in an encrypted channel
    server_cert: bytes

    #: The uuid of the client
    client_uuid: str

    #: The vendors URL
    vendor_url: str

    #: Client software version
    version: str

    #: Client description
    description: str

    #: Client name
    name: str

    #: Access to the configuration file used to store/read data in for this client
    sila2_config: ConfigParser

    #: The server port to which to connect
    server_port: Union[int, None]

    #: The server hostname to which to connect
    server_hostname: Union[str, None]

    def __init__(self,
                 name: str, description: str = "",
                 server_name: Optional[str] = None,
                 client_uuid: Optional[str] = None,
                 version: str = "0.0",
                 vendor_url: str = "",
                 server_hostname: str = "localhost", server_ip: str = '127.0.0.1', server_port: int = 50051,
                 cert_file: Optional[str] = 'sila_server.crt'):
        """

        :param name: Client name.
        :param description: Client description.
        :param server_name: If set, the client will try to auto-detect the servers IP and port in the network. Set to
                            None to disable auto-detection.
        :param client_uuid: The uuid of the client.
        :param version: Client software version.
        :param vendor_url: The vendors URL.
        :param server_hostname: The server hostname to which to connect. If the `server_ip` is given, it takes
                                precedence. Only used if `server_name` is None or auto-detection of the server fails.
        :param server_ip: The IP of the server to connect to. Only used if `server_name` is None or auto-detection of
                          the server fails.
        :param server_port: The port of the server. Only used if `server_name` is None or auto-detection of the server
                            fails.
        :param cert_file: The certificate file used to establish a secure connection to the server.
        """

        # read default values from config file
        self.sila2_config = read_config_file('client', name)

        # store the basic client data
        self.name = name
        self.description = description
        self.version = version
        self.vendor_url = vendor_url
        self.client_uuid = client_uuid if client_uuid is not None else self.sila2_config['server']['UUID']

        # networking
        self.server_hostname = None
        self.server_port = None
        #   Try to autodetect the server
        if server_name is not None:
            # TODO: Implement auto detection services
            # self.server_hostname = server_hostname
            # self.server_port = server_ports
            pass
        #   If auto detect was not active or failed, set manually
        if self.server_hostname is None:
            # decide whether to use ip or hostname
            if server_ip is not None and server_ip != '':
                if server_hostname is not None and server_hostname != '':
                    logging.info(
                        (
                            'Overwriting given hostname "{sila_hostname}" '
                            'with IP address "{ip}" since IP takes precedence.'
                        ).format(sila_hostname=server_hostname, ip=server_ip)
                    )
                self.server_hostname = server_ip
            else:
                self.server_hostname = server_hostname
            self.server_port = server_port

        # Encryption
        if cert_file is None:
            self.encryption = False
        else:
            try:
                with open(cert_file, 'rb') as file:
                    self.server_cert = file.read()
                self.encryption = True
            except FileNotFoundError as err:
                logging.error(
                    (
                        'Could not load encryption certificate, '
                        'no encryption will be used: {err}'
                    ).format(err=err))
                self.encryption = False

        # Connect
        if self.encryption:
            channel_credentials = grpc.ssl_channel_credentials(root_certificates=self.server_cert)

            self.channel = grpc.secure_channel(
                target='{hostname}:{port}'.format(
                    hostname=self.server_hostname,
                    port=self.server_port),
                credentials=channel_credentials
            )
        else:
            self.channel = grpc.insecure_channel(
                target='{hostname}:{port}'.format(
                    hostname=self.server_hostname,
                    port=self.server_port)
            )

        # Add base features the SiLAService functionality
        self.SiLAService_stub = SiLAService_feature_grpc.SiLAServiceStub(self.channel)
        self.SimulationController_stub = SimController_feature_grpc.SimulationControllerStub(self.channel)

        # Read the stimulation status of the server
        response = self.SimulationController_stub.Get_SimulationMode(
            SimController_feature_pb2.Get_SimulationMode_Parameters()
        )
        self._simulation_mode = response.SimulationMode.value

    @abstractmethod
    def run(self):
        """main gRPC client routine"""
        raise NotImplementedError

    @abstractmethod
    def stop(self, force: bool = False) -> bool:
        """
        Stop SiLA client routine

        :param force: If set True, the client is supposed to disconnect and stop immediately. Otherwise it can first try
                      to finish what it is doing.

        :returns: Whether the client could be stopped successfully or not.
        """
        raise NotImplementedError

    def switchToSimMode(self):
        """Switching to simulation mode"""
        logging.debug('Switching to simulation mode.')
        if not self._simulation_mode:
            self.SimulationController_stub.StartSimulationMode(
                SimController_feature_pb2.StartSimulationMode_Parameters()
            )
            self._simulation_mode = True

    def switchToRealMode(self):
        """Switching to real mode"""
        logging.debug('Switching to real mode.')
        if self._simulation_mode:
            self.SimulationController_stub.StartRealMode(
                SimController_feature_pb2.StartRealMode_Parameters()
            )
            self._simulation_mode = False

    def toggleSimMode(self):
        """Toggle between simulation and real mode"""
        logging.debug('Toggle of simulation/real mode requested:')
        if self._simulation_mode:
            self.switchToRealMode()
        else:
            self.switchToSimMode()

    @property
    def simulation_mode(self):
        return self._simulation_mode
