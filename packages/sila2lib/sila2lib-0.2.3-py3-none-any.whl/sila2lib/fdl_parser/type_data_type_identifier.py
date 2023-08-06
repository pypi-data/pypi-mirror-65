"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: References data type definitions in the data type attribute of SiLA elements.

:file:    type_data_type_identifier.py
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


class DataTypeIdentifier(DataType):
    """
    Class to reference a data type identifier
        This class simply represents a data type identifier, that must have been defined in the main part of the FDL
        file and allows to access the definition stored in an object of type class:`~.DataTypeDefinition`.

    .. seealso:: DataTypeDefinitions are read in the :class:`~.Command` class.
    """

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <DataTypeIdentifier>-xml element that contains this identifier.

        .. note:: For remaining parameters see :meth:`~.DataType.__init__`.
        """
        super().__init__(xml_tree_element=xml_tree_element)

        # Set specific data
        self.is_identifier = True

        # Set specific data
        self.sub_type = xml_tree_element.text

        # The name is simply equal to the underlying data type
        self.name = self.sub_type
