
from typing import Any, Callable, Dict

from .data_base import DataBase

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.type_constrained import ConstrainedType

from google.protobuf.message import Message


class DataConstrained(DataBase):

    feature: Any

    _function: Callable

    def __init__(self, identifier: str, content: ConstrainedType, feature_pb2: Any, fdl_parser: FDLParser):
        super().__init__(fdl_parser=fdl_parser)

        self.feature = feature_pb2
        self._function = feature_pb2

        self.sub_type = content.sub_type
        # create the containing type
        self.fields = {}
        obj = self.create_data_object(content=content.sub_type,
                                      identifier=identifier,
                                      feature=self._function,
                                      fdl_parser=self.fdl_parser)
        self.fields['constrained'] = obj

        # construct the paths to all low-level, basic data
        self.create_path()

    def __call__(self) -> Message:
        return self.fields['constrained']()

    def parse_from_message(self, message: Message):
        self.fields['constrained'].parse_from_message(message=message)

    @property
    def value(self) -> Dict[str, DataBase]:
        return self.fields

    @value.setter
    def value(self, values):
        raise NotImplementedError


def _create_constrained_data_object(content: ConstrainedType, identifier: str, feature: Any, fdl_parser: FDLParser) \
        -> DataConstrained:
    return DataConstrained(content=content,
                           identifier=identifier,
                           feature_pb2=feature,
                           fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(ConstrainedType, _create_constrained_data_object)
