
from typing import Optional
from typing import Dict, Any, Callable, Type

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.type_base import DataType

from abc import abstractmethod

from google.protobuf.message import Message


class DataBase:

    fields: Optional[Dict[str, 'DataBase']]

    paths: Dict[str, 'DataBase']

    #: Reference to the main FDLParser object from which this data element is created
    fdl_parser: FDLParser

    #: Path separator used to
    path_separator: str = '/'

    #: Class attribute to construct sub-types. Factory methods must be added at runtime
    factory_methods: Dict[type, Callable] = {}

    def __init__(self, fdl_parser: FDLParser):
        """Class initialiser."""
        self.fdl_parser = fdl_parser

    @classmethod
    def create_data_object(cls, content: DataType, identifier: str, feature: Any, fdl_parser: FDLParser) -> 'DataBase':
        content_type = type(content)
        if content_type in cls.factory_methods:
            return cls.factory_methods[content_type](content=content,
                                                     identifier=identifier,
                                                     feature=feature,
                                                     fdl_parser=fdl_parser)
        else:
            raise KeyError

    @classmethod
    def add_factory_method(cls, fdl_parser_type: Type[DataType], factory_method: Callable):
        cls.factory_methods[fdl_parser_type] = factory_method

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def parse_from_message(self, message: Message):
        raise NotImplementedError

    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, value: Any):
        raise NotImplementedError

    def get_value(self, path: str) -> Any:

        # If the path is empty, we want to return this objects value
        if not path:
            return self.value

        # try the fast track if the user wants to access low-level, basic data
        if path.lower() in self.paths:
            return self.paths[path].value

        # split the path in this objects field and the sub-objects
        field = path.split(sep=DataBase.path_separator, maxsplit=1)
        if field[0] in self.fields:
            return self.fields[field[0]].get_value(path=field[1])

        # unknown path
        raise KeyError

    def set_value(self, path: str, value: Any) -> None:

        # if the path is empty, try to set this objects value
        if not path:
            self.value = value

        # try the fast track
        if path in self.paths:
            self.paths[path].value = value
            return

        # work through the tree
        field = path.split(sep=DataBase.path_separator, maxsplit=1)
        if field[0] in self.fields:
            self.fields[field[0]].set_value(path=field[1], value=value)
            return

        raise KeyError

    def create_path(self) -> Dict[str, 'DataBase']:

        # initialise the dictionary for paths
        self.paths = {}

        # construct the path used
        for field_name in self.fields:
            for path, obj in self.fields[field_name].create_path().items():
                path = field_name + DataBase.path_separator + path
                self.paths[path.lower()] = obj

        return self.paths
