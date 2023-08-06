from typing import Callable, Generator
from typing import Union

import copy
from google.protobuf.message import Message

from .data.data_parameters import DataParameters
from .data.data_responses import DataResponses

from ..fdl_parser.fdl_parser import FDLParser
from ..fdl_parser.property import Property


class _DynamicProperty:

    #: Store whether this is an observable property
    observable: bool

    #: Store the parameters data type
    parameters: DataParameters

    #: Store the responses data type
    responses: DataResponses

    #: Reference to the main function calling the property
    _function: Union[Callable[[Message], Message], Generator[Message, None, None]]

    def __init__(self, property_element: Property, fdl_parser: FDLParser, feature_stub, feature_pb2):

        self.observable = property_element.observable

        # get the main function that calls the command
        if self.observable:
            _identifier = 'Subscribe_{id}'.format(id=property_element.identifier)
        else:
            _identifier = 'Get_{id}'.format(id=property_element.identifier)
        self._function = getattr(feature_stub, _identifier)

        # create the DataType for the parameters
        self.parameters = DataParameters(identifier=_identifier,
                                         content=None,
                                         feature_pb2=feature_pb2,
                                         fdl_parser=fdl_parser)

        # create the DataType for the responses
        self.responses = DataResponses(identifier=_identifier,
                                       content=[property_element.response],
                                       feature_pb2=feature_pb2,
                                       fdl_parser=fdl_parser)

    def __call__(self) -> Union[DataResponses, Generator[DataResponses, None, None]]:
        if self.observable:
            def generator_function() -> Generator[DataResponses, None, None]:
                for response in self._function(self.parameters()):

                    obj = copy.copy(self.responses)
                    obj.parse_from_message(message=response)

                    yield obj

            return generator_function()
        else:
            def static_function() -> DataResponses:
                response = self._function(self.parameters())

                obj = copy.copy(self.responses)
                obj.parse_from_message(message=response)

                return obj

            return static_function()
