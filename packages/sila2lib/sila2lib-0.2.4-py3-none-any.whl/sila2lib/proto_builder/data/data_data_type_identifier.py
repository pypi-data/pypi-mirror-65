
from typing import Any

from .data_base import DataBase

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.type_data_type_identifier import DataTypeIdentifier


def _create_data_type_identifier_data_object(content: DataTypeIdentifier, identifier: str, feature: Any,
                                             fdl_parser: FDLParser) -> DataBase:
    return DataBase.create_data_object(content=fdl_parser.data_type_definitions[content.sub_type].sub_type,
                                       identifier=identifier,
                                       feature=feature.__module__,
                                       fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(DataTypeIdentifier, _create_data_type_identifier_data_object)