"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: DataTypeDefinition element in a SiLA Feature Definition.

:file:    data_type_definition.py
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
from .type_basic import BasicType
from .type_list import ListType
from .type_constrained import ConstrainedType
from .type_structured import StructureType
from .type_data_type_identifier import DataTypeIdentifier


class DataTypeDefinition(DataType):
    """
    Class for data types that are defined directly inside the FDL file.
        This class stores information on data types that are defined in the FDL file so they can be reused in parameter
        or response definitions.

    .. seealso:: DataTypeDefinitions are read in the :class:`~.Command` class.
    """

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <DataTypeDefinition>-xml element that contains this identifier.

        :raises TypeError: No known sub-type found.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        self.is_sila_element = True

        # Every data type definition **must** have a DataType sub-element, so we create a sub-element from that
        if hasattr(xml_tree_element.DataType, 'Basic'):
            self.sub_type = BasicType(xml_tree_element=xml_tree_element.DataType.Basic)
        elif hasattr(xml_tree_element.DataType, 'List'):
            self.sub_type = ListType(xml_tree_element=xml_tree_element.DataType.List)
        elif hasattr(xml_tree_element.DataType, 'Structure'):
            self.sub_type = StructureType(xml_tree_element=xml_tree_element.DataType.Structure)
        elif hasattr(xml_tree_element.DataType, 'Constrained'):
            self.sub_type = ConstrainedType(xml_tree_element=xml_tree_element.DataType.Constrained)
        elif hasattr(xml_tree_element.DataType, 'DataTypeIdentifier'):
            self.sub_type = DataTypeIdentifier(xml_tree_element=xml_tree_element.DataType.DataTypeIdentifier)
        else:
            # invalid type
            raise TypeError
