"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Data type of a list format.

:file:    type_list.py
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

# import library packages
from .type_base import DataType
from . import type_basic as b_type
from . import type_structured as s_type
from . import type_constrained as c_type
from . import type_data_type_identifier as dti_type

# import custom exceptions
from .exceptions.exceptions import SubDataTypeError


class ListType(DataType):
    """
    Class to store the SiLA derived data type list.
    """

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <List>-xml element that contains this list type.

        :raises TypeError: Unknown sub-type found.
        :raises: SubDataTypeError: An invalid sub-type has been used.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_list = True

        # Every list **must** have a DataType sub-element, so we create a sub-element from that. However, this must not
        #   be a List itself
        if hasattr(xml_tree_element.DataType, 'Basic'):
            self.sub_type = b_type.BasicType(xml_tree_element=xml_tree_element.DataType.Basic)
        elif hasattr(xml_tree_element.DataType, 'List'):
            # Nested lists are not supported
            raise SubDataTypeError
        elif hasattr(xml_tree_element.DataType, 'Structure'):
            self.sub_type = s_type.StructureType(xml_tree_element=xml_tree_element.DataType.Structure)
        elif hasattr(xml_tree_element.DataType, 'Constrained'):
            self.sub_type = c_type.ConstrainedType(xml_tree_element=xml_tree_element.DataType.Constrained)
        elif hasattr(xml_tree_element.DataType, 'DataTypeIdentifier'):
            self.sub_type = dti_type.DataTypeIdentifier(xml_tree_element=xml_tree_element.DataType.DataTypeIdentifier)
        else:
            # invalid type
            raise TypeError('Sub-Element of the current list is of unknown type and can not be used.')
