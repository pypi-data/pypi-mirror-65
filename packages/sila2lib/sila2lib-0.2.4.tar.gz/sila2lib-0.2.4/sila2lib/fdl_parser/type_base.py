"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: (Abstract) base type for all data types.

:file:    type_base.py
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
from typing import Any, Union
from typing import List
from abc import ABC


class DataType(ABC):
    """
    Base class for storage of DataTypes.
        This class provides the universal attributes and functionality to represent DataType elements read from a FDL
        file.
    """

    # Allow some properties to easily give access to the type of this data type
    #: If this data type is a list of defined data
    is_list: bool = False
    #: If this data type is a structure containing multiple elements
    is_structure: bool = False
    #: If this data type is a constrained data type
    is_constrained: bool = False
    #: If this data type is a basic type (i.e. resolves to SiLA Framework definitions)
    is_basic: bool = False
    #: If this data type is just an identifier that must have been defined earlier
    is_identifier: bool = False
    #: SiLA Elements are XML elements that contain Identifier, DisplayName and a Description, thus this flag makes them
    #:   easy to find for additional output
    is_sila_element: bool = False

    #: Identifier used for this data type
    identifier: str

    #: Display name. If no display name is given, equal to the identifier
    name: str

    #: Description of the DataType
    description: str = ""

    #: The underlying type. For Base types this is only the SiLA2 defined names, but it can also be a nested object
    #:  (Structure, List, ...) or multiple sub_types in case of a structure
    sub_type: Union[str, 'DataType', List['DataType']]

    #: Reference to the xml tree element used to create this object
    _tree: Any

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The xml-Node that was used to construct this object.
        """
        self._tree = xml_tree_element

        # try to read Identifier, DisplayName and Description
        #   if they don't exist go for an empty string
        try:
            self.identifier = xml_tree_element.Identifier.text
        except AttributeError:
            self.identifier = ''

        try:
            self.name = xml_tree_element.DisplayName.text
        except AttributeError:
            self.name = ''

        try:
            self.description = xml_tree_element.Description.text
        except AttributeError:
            self.description = ''
