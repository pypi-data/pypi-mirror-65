"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA device detection library*

:details: SiLA Device detection is based on zeroconf / bonjour.
          s. zeroconf documentation for details.
          server looks for services in local network
          server chooses a free port
          server receives a logical name
          client can use this logicial name to address server

:file:    sila_device_detection.py
:authors: mark doerr (mark@uni-greifswald.de)

:date: (creation)          20180530
:date: (last modification) 2019-11-09

.. note:: -
.. todo:: - check available ports and select first free port available
________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.0.6"

import socket
from zeroconf import ServiceInfo, Zeroconf

import logging

class SiLA2ServiceDetection():
    """ This class Registers the SiLA2 service in the given network  """
    def __init__ (self):
        """ zeroconfig service regitration """

        self.service_tag = "_sila._tcp.local."

    def registerService(self, service_name="SiLATestService",
                         IP="127.0.0.1",
                         port=None,
                         description={'version': '0.0.1', 'descr1': 'description 1', 'descr2': 'description 2'},
                         server_uuid=None):
        """ :param [param_name]: [description]"""

        # check, if port is already used, otherwise assign new port

        if port is None:
            # randomly assign port between 50001 and 50999
            from random import randint
            port = randint(55001, 55999) # please make a better choice according to given port standards

        zc = Zeroconf()
        logging.debug("UUID: {}".format(server_uuid))
        self.ser_info = ServiceInfo( self.service_tag,
                           "{server_uuid}.{service_tag}".format(server_uuid=server_uuid, service_tag=self.service_tag),
                           socket.inet_aton(IP), port, 0, 0, description)

        logging.info("registratering the SiLA2 service {} in the network...{} with port {}".format(service_name, IP, port ) )

        zc.register_service(self.ser_info)

        logging.info("Registration done ..." )


    def findServiceByName(self, service_name=""):
        """ this method tries to find a given service by name and returns the connection parameters
        :param service_name [string]: service name to search for"""

        logging.info("not implemented yet ... just sending default values..")

        return { 'server_name':'localhost', 'port':50001  }

    def watchForNewServices(self):
        """ new service watcher
        if server is removed from server list, send a gRPC ping (s. unitelabs implementation)
        this should be called every second
        :param [param_name]: [description]"""
        pass
