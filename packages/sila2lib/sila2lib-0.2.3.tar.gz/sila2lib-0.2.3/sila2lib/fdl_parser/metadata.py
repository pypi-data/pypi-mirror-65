"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Metadata element in a SiLA Feature Definition.

:file:    metadata.py
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
from typing import Any
from typing import List

# import library packages
from .data_type_parameter import ParameterDataType


class Metadata:
    """
    This class stores all information corresponding to **one** metadata element defined in the feature definition.

    .. note:: This class was introduced for the SiLA standard staring at version 0.2.
    """
    #: Identifier of the metadata elements
    identifier: str

    #: Display name property of the metadata
    name: str

    #: Metadata description
    description: str

    #: Reference to the xml-tree of the property
    _tree: Any

    #: The parameter defined for this metadata element
    parameter: ParameterDataType

    #: List of all defined execution errors (identifiers) that can occur during reading of this property (SiLA v0.2)
    defined_execution_errors: List[str]

    def __init__(self, xml_tree_element):
        """
        Class initialiser

        :param xml_tree_element: The contents of the <Property>-xml node
        """
        self._tree = xml_tree_element

        self.identifier = xml_tree_element.Identifier.text
        self.name = xml_tree_element.DisplayName
        self.description = xml_tree_element.Description

        self.parameter = ParameterDataType(xml_tree_element=xml_tree_element)

        # get all defined execution errors
        self.defined_execution_errors = []
        if hasattr(xml_tree_element, 'DefinedExecutionErrors'):
            for defined_error in xml_tree_element.DefinedExecutionErrors.Identifier:
                self.defined_execution_errors.append(defined_error.text)
