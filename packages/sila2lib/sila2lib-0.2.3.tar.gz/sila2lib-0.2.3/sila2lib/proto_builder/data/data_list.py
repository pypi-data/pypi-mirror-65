
from typing import Any, Callable, Dict, List

from .data_base import DataBase

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.type_list import ListType

from google.protobuf.message import Message

import copy


class DataList(DataBase):

    feature: Any

    _function: Callable

    #: A default object that is stored in this class. This is necessary to have a sample object based on which copies
    #:  can be created
    default: DataBase

    def __init__(self, identifier: str, content: ListType, feature_pb2: Any, fdl_parser: FDLParser):
        super().__init__(fdl_parser=fdl_parser)

        self.feature = feature_pb2
        self._function = feature_pb2

        self.sub_type = content.sub_type
        # create one sample of the containing type
        self.fields = {}
        obj = self.create_data_object(content=content.sub_type,
                                      identifier=identifier,
                                      feature=self._function,
                                      fdl_parser=self.fdl_parser)
        self.default = obj

        # due to the fact that this is a list, no direct path access is possible
        self.paths = {}

    def __call__(self) -> List[Message]:
        return [element() for element in self.fields.values()]

    def parse_from_message(self, message: List[Message]):
        # clear the current data
        self.fields = {}
        # rewrite
        for index, element in enumerate(message):
            # create a copy of the default element and work on that
            obj = copy.copy(self.default)
            obj.parse_from_message(message=element)
            self.fields[str(index)] = obj

    def get_value(self, path: str) -> Any:
        # if the list is requested handle this here
        if path.lower() == 'list':
            return self.value

        # otherwise try to resolve it the "normal" way
        return super().get_value(path)

    def set_value(self, path: str, value: Any) -> None:
        if path.lower() == 'list':
            self.value = value

        super().set_value(path, value)

    def create_path(self) -> Dict[str, DataBase]:
        """
        Returns the path to this object.

        :returns: The path and a reference to this object.

        .. note:: For this class we have to overwrite the :meth:`DataBase.get_path` method, since it returns its own
                  content that does not depend on the fields variable.
                  A further access is not directly possible, since the field can contain numerous values. it can however
                  be accessed by getting this module and evaluating it's path property.
        """
        return {'List': self}

    @property
    def value(self) -> List[Any]:
        return list(self.fields.values())

    @value.setter
    def value(self, values: List[Any]):
        # empty the current list first before filling it
        self.fields = {}
        for index, value in enumerate(values):
            self.fields[str(index)] = value


def _create_list_data_object(content: ListType, identifier: str, feature: Any, fdl_parser: FDLParser) -> DataList:
    return DataList(content=content,
                    identifier=identifier,
                    feature_pb2=feature,
                    fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(ListType, _create_list_data_object)
