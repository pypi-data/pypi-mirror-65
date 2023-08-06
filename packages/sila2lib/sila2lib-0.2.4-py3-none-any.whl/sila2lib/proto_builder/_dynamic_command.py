from typing import Optional, Union
from typing import Callable

import copy
import time
from google.protobuf.message import Message

from .data.data_parameters import DataParameters
from .data.data_responses import DataResponses
from .data.data_intermediates import DataIntermediates

from ..fdl_parser.fdl_parser import FDLParser
from ..fdl_parser.command import Command

from ..framework import SiLAFramework_pb2 as silaFW_pb2


class _DynamicCommand:

    #: Store whether this is an observable command
    observable: bool

    #: Store the parameters data type
    parameters: DataParameters

    #: Store the responses data type
    responses: DataResponses

    #: Store the intermediate responses data type (or none if not observable)
    intermediate_responses: Optional[DataIntermediates]

    #: Reference to the main function calling the command
    _function: Callable[[Message], Union[Message, silaFW_pb2.CommandConfirmation]]

    # For observable commands, define more Callable functions
    #: Reference for the intermediate call to an observable command
    _intermediate: Optional[Callable[[silaFW_pb2.CommandExecutionUUID], Message]]

    #: Reference to the info call of an observable command
    _info: Optional[Callable[[silaFW_pb2.CommandExecutionUUID], silaFW_pb2.ExecutionInfo]]

    #: Reference to the result call of an observable command
    _result: Optional[Callable[[silaFW_pb2.CommandExecutionUUID], Message]]

    def __init__(self, command: Command, fdl_parser: FDLParser, feature_stub, feature_pb2):

        self.observable = command.observable

        # get the main function that calls the command
        self._function = getattr(feature_stub, command.identifier)
        if self.observable:
            # for observable commands we need to obtain a bit more
            if hasattr(feature_stub, '{id}_Intermediate'.format(id=command.identifier)):
                # intermediate responses are optional
                self._intermediate = getattr(feature_stub, '{id}_Intermediate'.format(id=command.identifier))
            else:
                self._intermediate = None
            self._info = getattr(feature_stub, '{id}_Info'.format(id=command.identifier))
            self._result = getattr(feature_stub, '{id}_Result'.format(id=command.identifier))

        # create the DataType for the parameters
        content = list(command.parameters.values())
        if content[0].sub_type.sub_type == 'Void':
            # no parameter given for the command
            content = None
        self.parameters = DataParameters(identifier=command.identifier,
                                         content=content,
                                         feature_pb2=feature_pb2,
                                         fdl_parser=fdl_parser)

        # create the DataType for the responses
        content = list(command.responses.values())
        if content[0].sub_type.sub_type == 'Void':
            # no response given for the command
            content = None
        self.responses = DataResponses(identifier=command.identifier,
                                       content=content,
                                       feature_pb2=feature_pb2,
                                       fdl_parser=fdl_parser)

        if self.observable:
            # create the data type for the intermediate responses
            self.intermediate_responses = DataIntermediates(identifier=command.identifier,
                                                            content=list(command.intermediates.values()),
                                                            feature_pb2=feature_pb2,
                                                            fdl_parser=fdl_parser)
        else:
            self.intermediate_responses = None

    def __call__(self, parameters: Optional[Union[DataParameters, Message]] = None, block: bool = False) \
            -> Union[silaFW_pb2.CommandConfirmation, DataResponses]:

        # see what kind of parameter we got
        if parameters is None:
            _parameters = self.parameters()
        elif type(parameters) is DataParameters:
            _parameters = parameters()
        elif type(parameters) is Message:
            # we assume the correct message has been passed
            _parameters = parameters
        else:
            raise TypeError

        response = self._function(_parameters)

        if self.observable:
            if block:
                # block, so we wait until we have a result
                command_uuid = response.commandExecutionUUID.value

                for progress in self._info(silaFW_pb2.CommandExecutionUUID(value=command_uuid)):
                    if (progress.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.waiting) or \
                            (progress.commandStatus == silaFW_pb2.ExecutionInfo.CommandStatus.running):
                        time.sleep(0.1)
                    else:
                        break
                    # Note: This has no timeout, so it could run infinitely if the server somehow fails
                # progress finished, so let us try and get a result
                response = self._result(silaFW_pb2.CommandExecutionUUID(value=command_uuid))
            else:
                # do not block, just return the command confirmation
                return response

        # If we have come here, we have the declared response data type, so we can parse it and return it
        obj = copy.copy(self.responses)
        obj.parse_from_message(message=response)

        return obj

    def info(self, command_uuid: str) -> silaFW_pb2.ExecutionInfo:
        if not self.observable:
            raise TypeError

        return self._info(silaFW_pb2.CommandExecutionUUID(value=command_uuid))

    def intermediate(self, command_uuid: str) -> Optional[DataIntermediates]:
        if not self.observable:
            raise TypeError

        if self._intermediate is None:
            return None

        response = self._intermediate(silaFW_pb2.CommandExecutionUUID(value=command_uuid))

        obj = copy.copy(self.intermediate_responses)
        obj.parse_from_message(message=response)

        return obj

    def result(self, command_uuid: str) -> DataResponses:
        if not self.observable:
            raise TypeError
        response = self._result(silaFW_pb2.CommandExecutionUUID(value=command_uuid))

        obj = copy.copy(self.responses)
        obj.parse_from_message(message=response)

        return obj

    def get_parameter(self) -> DataParameters:
        """
        Return a copy of the parameters object.
        Creates a copy of the (default) parameters object for the user to change, the way over this method is preferred
            since it will not change the default implementation.
            The object obtained this way can be used to modify parameter values and then as input to the __call__
            function.
        """
        return copy.copy(self.parameters)
