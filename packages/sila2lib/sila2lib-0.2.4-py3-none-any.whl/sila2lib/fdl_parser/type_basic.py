"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Basic data type for all standard SiLA data types.

:file:    type_basic.py
:authors: Timm Severin

:date: (creation)          20190820
:date: (last modification) 20190820

__________________________________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
__________________________________________________________________________________________________
"""

# import general packages
import datetime

# import meta packages
from typing import Any

# import package related packages
from .type_base import DataType


class BasicType(DataType):
    """
    Class for the basic data type as defined in the SiLA standards.
    """

    #: Default value, only available for BasicTypes
    default_value: Any

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <Basic>-xml element that contains this basic type.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.

        .. note:: Date, Time and Timestamp follow the
                  `W3C format for .xsd <https://www.w3.org/TR/xmlschema11-2/#dateTime>`_
                  files which in turn relies on `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_basic = True
        self.sub_type = xml_tree_element.text

        # The name is simply equal to the underlying data type
        self.name = self.sub_type

        # and now distinguish between the named types
        if self.sub_type == 'Boolean':
            self.description = "Basic logic/boolean type"
            self.default_value = False
        elif self.sub_type == 'Integer':
            self.description = ''
            self.default_value = 0
        elif self.sub_type == 'Real':
            self.description = 'Basic float/double type'
            self.default_value = 0.0
        elif self.sub_type == 'String':
            self.description = 'Basic string type'
            self.default_value = "'default string'"
        elif self.sub_type == 'Binary':
            self.description = 'Basic byte type'
            self.default_value = b""
        elif self.sub_type == 'Void':
            self.description = 'Void/empty type'
            self.default_value = b""
        elif self.sub_type == 'Date':
            self.description = 'Basic date type'
            self.default_value = datetime.datetime.utcnow().strftime('%Y-%m-%d+0000')
        elif self.sub_type == 'Time':
            self.description = 'Basic time type'
            self.default_value = datetime.datetime.utcnow().strftime('%H:%M:%S+0000')
        elif self.sub_type == 'Timestamp':
            self.description = 'Basic timestamp type'
            self.default_value = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000')
        else:
            raise TypeError
