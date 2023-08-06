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
from typing import Dict

# import general packages
import warnings

from .exceptions.exceptions import ConstraintUnsupportedContentType


class ConstraintContentType:
    """
    The class to store ContentType constraints.
        Content types are usually found as ContentType: type/subtype; *parameters.
        Examples: ContentType=text/html; charset=utf-8

    The SiLA standard officially supports the content types:

        * ``application/xml``
        * ``application/x-animl``
        * ``application/json``
    """

    #: The main type of the ContentType that is allowed (e.g. 'text')
    type: str

    #: The subtype of the ContentType that is allowed (e.g. 'html')
    subtype: str

    #: Additional parameters for the content type (e.g. 'charset': 'utf-8')
    parameters: Dict[str, str]

    def __init__(self, xml_tree_element):
        """
        Class initialiser.

        :param xml_tree_element: The content of this <ContentType>-xml element that contains this constraint.
        """

        official_content_types = ["application/xml", "application/x-animl", "application/json"]

        self.type = xml_tree_element.Type.text
        self.subtype = xml_tree_element.Subtype.text

        if (self.type + "/" + self.subtype).lower() not in official_content_types:
            warnings.warn(
                (
                    'The given content type constraint is for a content type that is not officially supported '
                    '(ContentType: {type}/{subtype}).'
                    'It will be stored anyway, proper execution can not be ensured. '
                ).format(
                    type=self.type,
                    subtype=self.subtype
                ),
                ConstraintUnsupportedContentType
            )

        self.parameters = {}
        if hasattr(xml_tree_element, 'Parameters'):
            for parameter in xml_tree_element.Parameters.Parameter:
                self.parameters[parameter.Attribute.text] = parameter.Value.text
