"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Simulation controller for SiLA server*

:details: This Feature provides control over the simulation behaviour of a SiLA Server.

            A SiLA Server can run in two modes:
            (a) a real mode - with real activities, e.g. addressing or controlling real hardware,
            writing to real databases, moving real plates etc.
            (b) a simulation mode - where every command is only simulated and responses are just example returns.

            Note that certain commands and properties might not be affected by this feature if they
            do not interact with the real world.
           
:file:    SimulationController.py
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

__version__ = "0.2.0"

import logging
import grpc
from typing import Optional

from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2

# importing protobuf and gRPC handler/stubs
from . import SimulationController_pb2 as pb2
from . import SimulationController_pb2_grpc as pb2_grpc


class SimulationController(pb2_grpc.SimulationControllerServicer):
    """
    SimulationController: This Feature provides control over the simulation behaviour of a SiLA Server.

    A SiLA Server can run in two modes:
    (a) a real mode - with real activities, e.g. addressing or controlling real hardware,
    writing to real databases, moving real plates etc.
    (b) a simulation mode - where every command is only simulated and responses are just example returns.

    Note that certain commands and properties might not be affected by this feature if they
    do not interact with the real world.
    """
    #: Current state of the server
    simulation_mode: bool

    #: Reference to the SiLA server
    sila_server: 'SiLA2Server'

    def __init__(self, sila2_server: 'SiLA2Server', simulation_mode: bool = True):
        """
        SimulationController class initialiser.

        :param sila2_server: The SiLA2 Server object for which this simulation controller is responsible.
        :param simulation_mode: Start in simulation mode or not.
        """
        logging.debug("Initialising org.silastandard feature: SimulationController.")

        self.sila_server = sila2_server
        self.simulation_mode = simulation_mode

    def StartSimulationMode(self, request=None, context: Optional[grpc.ServicerContext] = None) \
            -> pb2.StartSimulationMode_Responses:
        """
        Starting server into simulation mode with the following procedure, if the server was in real mode:
        - Terminate all running  commands that alter real world data or matter.
        - Cancel all dynamic property subscriptions that use real world data.
        
        :param request: gRPC request. This argument is optional and not required, so the function can be called with
                                      arguments in case they are called internally.
        :param context: gRPC context. This argument is optional and not required, so the function can be called with
                                      arguments in case they are called internally.
        """
        logging.debug("StartSimulationMode()")
        
        if self.sila_server._switch_to_simulation_mode():
            self.simulation_mode = True

        return pb2.StartSimulationMode_Responses()

    def StartRealMode(self, request=None, context: Optional[grpc.ServicerContext] = None) \
            -> pb2.StartRealMode_Responses:
        """
        Starting server into real mode with the following procedure:
        - Terminate all simulated commands and properties
        - If real world is ready (e.g. databases or hardware): Accept new commands and property retrievals.

        :param request: gRPC request. This argument is optional and not required, so the function can be called with
                                      arguments in case they are called internally.
        :param context: gRPC context. This argument is optional and not required, so the function can be called with
                                      arguments in case they are called internally.
        """
        logging.debug("StartRealMode()")

        if self.sila_server._switch_to_real_mode():
            self.simulation_mode = False

        return pb2.StartRealMode_Responses()

    def Get_SimulationMode(self, request, context: grpc.ServicerContext) -> pb2.Get_SimulationMode_Responses:
        """
        Indication whether SiLA Server is in Simulation Mode or not.

        :param request: gRPC request
        :param context: gRPC context

        :returns:
            response.SimulationMode: Indication whether SiLA Server is in Simulation Mode or not.
        """
        logging.debug("Get_SimulationMode: {mode}".format(mode="True" if self.simulation_mode else "False"))

        return pb2.Get_SimulationMode_Responses(
            SimulationMode=silaFW_pb2.Boolean(value=self.simulation_mode)
        )
