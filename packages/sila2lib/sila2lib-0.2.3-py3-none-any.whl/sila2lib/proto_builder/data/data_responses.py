
from typing import Optional
from typing import Any, Callable, Dict, Iterable

from .data_base import DataBase

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.data_type_response import ResponseDataType

from google.protobuf.message import Message


class DataResponses(DataBase):

    feature: Any

    _function: Callable

    def __init__(self, identifier: str, content: Optional[Iterable[ResponseDataType]],
                 feature_pb2: Any, fdl_parser: FDLParser):
        super().__init__(fdl_parser=fdl_parser)

        self.feature = feature_pb2

        # construct the local (protobuf) identifier used
        _identifier = "{identifier}_Responses".format(identifier=identifier)

        self._function = getattr(self.feature, _identifier)

        # create the containing type
        self.fields = {}
        if content is not None:
            # allow for empty responses
            for response in content:
                obj = self.create_data_object(content=response.sub_type,
                                              identifier=response.identifier,
                                              feature=self._function,
                                              fdl_parser=self.fdl_parser)
                self.fields[response.identifier] = obj

        # construct the paths to all low-level, basic data
        self.create_path()

    def __call__(self) -> Message:
        # evaluate the fields
        _fields = {key: value() for (key, value) in self.fields.items()}

        return self._function(**_fields)

    def parse_from_message(self, message: Message):
        for field in self.fields:
            if message.HasField(field):
                self.fields[field].parse_from_message(message=getattr(message, field))
    
    @property
    def value(self) -> Dict[str, DataBase]:
        return self.fields

    @value.setter
    def value(self, value):
        raise NotImplementedError


def _create_response_data_object(content: Optional[Iterable[ResponseDataType]], identifier: str,
                                 feature: Any, fdl_parser: FDLParser) \
        -> DataResponses:
    return DataResponses(content=content,
                         identifier=identifier,
                         feature_pb2=feature,
                         fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(ResponseDataType, _create_response_data_object)
