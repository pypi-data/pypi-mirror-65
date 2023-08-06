"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Module to store ContentType constraints.

:file:    constraint_content_type.py
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
from typing import Optional

# import general packages
from enum import Enum


class SchemaType(Enum):
    """
    Enumeration for the different types of schemata that are allowed.
    """
    XML = 'Xml'
    JSON = 'Json'


class ConstraintSchema:
    """
    Class to store Schema constraints.

    The type can be either 'Xml' or 'Json'. The data can be passed either as an url or inline.
    """

    #: Type of the schema definition
    type: SchemaType

    #: The url from where to load the schema data
    url: Optional[str]

    #: The inline schema data
    inline: Optional[str]

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <Schema>-xml element that contains this constraint.

        :raises KeyError: The given schema type is invalid (Only Xml, Json allowed).
        :raises TypeError: The data was given in an invalid format (only Url, Inline allowed).
        """

        self.type = SchemaType[xml_tree_element.Type.text.upper()]

        if hasattr(xml_tree_element, 'Url'):
            self.url = xml_tree_element.Url.text
            self.inline = None
        elif hasattr(xml_tree_element, 'Inline'):
            self.inline = xml_tree_element.Inline.text
            self.url = None
        else:
            raise TypeError('No valid schema data found.')
