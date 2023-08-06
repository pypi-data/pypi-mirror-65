"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Structured data type in SiLA elements.

:file:    type_structured.py
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

# import meta packages
from typing import List

# import library packages
from .type_base import DataType
from . import type_basic as b_type
from . import type_list as l_type
from . import type_constrained as c_type
from . import type_data_type_identifier as dti_type


class StructureType(DataType):
    """
    Class for the derived SiLA data type that implements a structure.
        A structure can contain many elements, which is why to access those multiple levels must be stepped through. The
        sub-type of this DataType is only a List that refers to all :class:`StructureElementType` Elements. These again
        contain a sub-type that represents the actual element.
    """

    #: The underlying type here is always a list of :class:`StructureElementType` objects.
    sub_type: List['StructureElementType']

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <Structure>-xml element that contains this structure type.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_structure = True

        # Structures can have an arbitrary number of elements, let's figure them out
        self.sub_type = []
        for element_index in range(0, len(xml_tree_element.Element)):
            self.sub_type.append(
                StructureElementType(xml_tree_element=xml_tree_element.Element[element_index])
            )


class StructureElementType(DataType):
    """
    Class that represents a single element of a structure.
    """

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <Structure><Element>-xml element that contains this elements info.

        :raises TypeError: Unknown sub-type found.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        self.is_sila_element = True

        # Every element **must** have a DataType sub-element, so we create a sub-element from that
        if hasattr(xml_tree_element.DataType, 'Basic'):
            self.sub_type = b_type.BasicType(xml_tree_element=xml_tree_element.DataType.Basic)
        elif hasattr(xml_tree_element.DataType, 'List'):
            self.sub_type = l_type.ListType(xml_tree_element=xml_tree_element.DataType.List)
        elif hasattr(xml_tree_element.DataType, 'Structure'):
            self.sub_type = StructureType(xml_tree_element=xml_tree_element.DataType.Structure)
        elif hasattr(xml_tree_element.DataType, 'Constrained'):
            self.sub_type = c_type.ConstrainedType(xml_tree_element=xml_tree_element.DataType.Constrained)
        elif hasattr(xml_tree_element.DataType, 'DataTypeIdentifier'):
            self.sub_type = dti_type.DataTypeIdentifier(xml_tree_element=xml_tree_element.DataType.DataTypeIdentifier)
        else:
            # invalid type
            raise TypeError
