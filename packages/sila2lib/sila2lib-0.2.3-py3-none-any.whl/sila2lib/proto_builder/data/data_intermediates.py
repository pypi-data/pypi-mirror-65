
from typing import Any, Callable, Dict, Iterable

from .data_base import DataBase

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.data_type_intermediate import IntermediateDataType

from google.protobuf.message import Message


class DataIntermediates(DataBase):

    feature: Any

    _function: Callable

    def __init__(self, identifier: str, content: Iterable[IntermediateDataType], feature_pb2: Any, fdl_parser: FDLParser):
        super().__init__(fdl_parser=fdl_parser)

        self.feature = feature_pb2

        # construct the local (protobuf) identifier used
        _identifier = "{identifier}_IntermediateResponses".format(identifier=identifier)

        self._function = getattr(self.feature, _identifier)

        # create the containing type
        self.fields = {}
        for intermediate in content:
            obj = self.create_data_object(content=intermediate.sub_type,
                                          identifier=intermediate.identifier,
                                          feature=self._function,
                                          fdl_parser=self.fdl_parser)
            self.fields[intermediate.identifier] = obj

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


def _create_intermediate_data_object(content: Iterable[IntermediateDataType], identifier: str,
                                     feature: Any, fdl_parser: FDLParser) \
        -> DataIntermediates:
    return DataIntermediates(content=content,
                             identifier=identifier,
                             feature_pb2=feature,
                             fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(IntermediateDataType, _create_intermediate_data_object)
