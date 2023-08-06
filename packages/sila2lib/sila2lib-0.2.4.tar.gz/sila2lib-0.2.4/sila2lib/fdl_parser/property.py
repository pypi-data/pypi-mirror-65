"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Property element in a SiLA Feature Definition.

:file:    property.py
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
from .data_type_response import ResponseDataType


class Property:
    """
    This class stores all information corresponding to **one** property defined in the feature definition.
    """
    #: Identifier of the property
    identifier: str

    #: Display name property of the property
    name: str

    #: Property description
    description: str

    #: Is this an observable property
    observable: bool

    #: Reference to the xml-tree of the property
    _tree: Any

    #: The response defined for this property
    response: ResponseDataType

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

        self.observable = xml_tree_element.Observable.text.lower() == 'yes'

        self.response = ResponseDataType(xml_tree_element=xml_tree_element)

        # get errors
        self.defined_execution_errors = []
        if hasattr(xml_tree_element, 'DefinedExecutionErrors'):
            for defined_error in xml_tree_element.DefinedExecutionErrors.Identifier:
                self.defined_execution_errors.append(defined_error.text)
