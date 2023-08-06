"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Element for all errors defined in a SiLA Feature Definition.

:file:    standard_error.py
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


class StandardError:
    """Base class for all standard errors that are defined."""

    #: Identifier of the standard error
    identifier: str

    #: Display name property of the standard error
    name: str

    #: Standard error description
    description: str

    #: Reference to the xml-tree of the property
    _tree: Any

    def __init__(self, xml_tree_element):
        """
        Class initialiser

        :param xml_tree_element: The contents of the <Property>-xml node
        """
        self._tree = xml_tree_element

        self.identifier = xml_tree_element.Identifier.text
        self.name = xml_tree_element.DisplayName
        self.description = xml_tree_element.Description


class DefinedExecutionError(StandardError):
    """
    Storage class for defined execution errors.
        This class can be used to store all standard execution errors that occur while executing a command or reading a
        property. Consequently, these objects are usually created by the :class:`~.Command` and :class:`~.Property` #
        classes. Since this class has no special properties, it is effectively the identical implementation to any
        :class:`StandardError`

    .. note:: This class supersedes the :class:`StandardReadError` and :class:`StandardExecutionError` classes that were
              used in the version 0.1 of the SiLA standard.
    """
