
from typing import Any, Dict
from typing import Union

import datetime

from google.protobuf.message import Message

from .data_base import DataBase

from ...framework import SiLAFramework_pb2 as silaFW_pb2

from ...fdl_parser.fdl_parser import FDLParser
from ...fdl_parser.type_basic import BasicType


class DataBasic(DataBase):

    type: str

    _value: Any

    def __init__(self, content: BasicType, fdl_parser: FDLParser):
        super().__init__(fdl_parser=fdl_parser)
        self.type = content.name
        self.value = content.default_value
        self.fields = None

    def __call__(self) -> Message:
        if self.type == 'String':
            return silaFW_pb2.String(value=self.value)
        elif self.type == 'Integer':
            return silaFW_pb2.Integer(value=self.value)
        elif self.type == 'Real':
            return silaFW_pb2.Real(value=self.value)
        elif self.type == 'Boolean':
            return silaFW_pb2.Boolean(value=self.value)
        elif self.type == 'Binary':
            return silaFW_pb2.Binary(value=self.value)
        elif self.type == 'Date':
            return silaFW_pb2.Date(day=self.value.day, month=self.value.month, year=self.value.year,
                                   timezone=self._get_timezone(date=self.value))
        elif self.type == 'Time':
            return silaFW_pb2.Time(second=self.value.second, minute=self.value.minute, hour=self.value.hour,
                                   timezone=self._get_timezone(date=self.value))
        elif self.type == 'Timestamp':
            return silaFW_pb2.Timestamp(second=self.value.second, minute=self.value.minute, hour=self.value.hour,
                                        day=self.value.day, month=self.value.month, year=self.value.year,
                                        timezone=self._get_timezone(date=self.value))
        else:
            raise TypeError

    def parse_from_message(self, message: Message):
        if message.DESCRIPTOR.name == self.type:
            if self.type in ['Date', 'Time', 'Timestamp']:
                # we let the setter handle the type conversion
                #  TODO: I assume this does not work, handling of date-link things is not completely consistent I fear
                self.value = getattr(message, self.type)
            else:
                # extract the value here
                # self.value = getattr(message, self.type).value
                self.value = message.value

    def get_value(self, path: str) -> Any:
        if not path == self.type or not path:
            raise TypeError

        return self.value

    def set_value(self, path: str, value: Any) -> None:
        if not path == self.type or not path:
            raise TypeError

        self.value = value

    def create_path(self) -> Dict[str, 'DataBasic']:
        """
        Returns the path to this object.

        :returns: The path and a reference to this object.

        .. note:: For this class we have to overwrite the :meth:`DataBase.get_path` method, since it returns its own
                  content that does not depend on the fields variable.
                  This is necessary to stop the recursion of the :meth:`DataBase.get_path` method into the sub-levels
                  of the object hierarchy.
        """
        return {self.type: self}

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        if self.type == 'String':
            self._value = str(value)
        elif self.type == 'Integer':
            self._value = int(value)
        elif self.type == 'Real':
            self._value = float(value)
        elif self.type == 'Boolean':
            if isinstance(value, str):
                self._value = True if value.lower().strip() == 'true' else False
            else:
                self._value = True if value else False
        elif self.type == 'Binary':
            self._value = bytes(value)
        elif self.type == 'Date':
            self._value = self._input_to_datetime(value, 'date')
        elif self.type == 'Time':
            self._value = self._input_to_datetime(value, 'time')
        elif self.type == 'Timestamp':
            self._value = self._input_to_datetime(value, 'datetime')
        else:
            raise TypeError

    @staticmethod
    def _get_timezone(date: datetime.datetime) -> silaFW_pb2.Timezone:
        return silaFW_pb2.Timezone(
            hours=int(date.utcoffset().seconds / 3600),
            minutes=(date.utcoffset().seconds / 60) % 60
        )

    @staticmethod
    def _input_to_datetime(value: Union[str, datetime.date,
                                        silaFW_pb2.Time, silaFW_pb2.Date, silaFW_pb2.Timestamp],
                           target: str) \
            -> datetime.datetime:

        date_strings = {
            'date': ['%Y-%m-%d%z', '%Y-%m-%d'],         # Year, month, day; optionally a timezone
            'time': ['%H:%M:%S%z', '%H:%M:%S',          # Hour, minute and second, optionally a timezone
                     '%H:%M%z', '%H:%M'],               # Only hour and minute, second = 0, optionally a timezone
            'timestamp': ['%Y-%m-%dT%H:%M%S%z', '%Y-%m-%dT%H:%M%S']  # iso format, optionally a timezone
        }

        if (isinstance(value, datetime.date) and (target == 'date')) or \
                (isinstance(value, datetime.time) and (target == 'time')) or \
                isinstance(value, datetime.datetime):
            # can be: datetime.datetime, datetime.date
            #   we can store them directly
            _date = value
        elif isinstance(value, (silaFW_pb2.Time, silaFW_pb2.Date, silaFW_pb2.Timestamp)):

            def get_message_attr(field: str, default: int) -> int:
                """Helper function to get a default value if the actual value is 0 (default int n proto3)"""
                field_value = getattr(value, field)
                return field_value if not field_value == 0 else default

            if target == 'date':
                _date = datetime.datetime(year=get_message_attr('year', 1900),
                                          month=get_message_attr('month', 1),
                                          day=get_message_attr('day', 1))
            elif target == 'time':
                _date = datetime.datetime(year=1900, month=1, day=1,
                                          hour=get_message_attr('hour', 0),
                                          minute=get_message_attr('minute', 0),
                                          second=get_message_attr('second', 0))
            else:
                # Either target == 'timestamp' or simple fail-safe default
                _date = datetime.datetime(year=get_message_attr('year', 1900),
                                          month=get_message_attr('month', 1),
                                          day=get_message_attr('day', 1),
                                          hour=get_message_attr('hour', 0),
                                          minute=get_message_attr('minute', 0),
                                          second=get_message_attr('second', 0))
        elif isinstance(value, str):
            success = False
            for date_format in date_strings[target]:
                try:
                    _date = datetime.datetime.strptime(value, date_format)
                except ValueError:
                    # this parsing failed, just try another option
                    pass
                else:
                    success = True
                    break
            if not success:
                # re-raise the value error that the input could not be parsed
                raise ValueError
        else:
            raise TypeError

        # if no information on the timezone is given, assume we work with UTC
        if _date.tzinfo is None:
            _date.replace(tzinfo=datetime.timezone(offset=datetime.timedelta(hours=0)))

        return _date


def _create_basic_data_object(content: BasicType, identifier: str, feature: Any, fdl_parser: FDLParser) -> DataBasic:
    return DataBasic(content=content, fdl_parser=fdl_parser)


# register the factory method for this object
DataBase.add_factory_method(BasicType, _create_basic_data_object)
