"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Response data type in a SiLA Command, Property, Intermediate, ...

:file:    data_type_response.py
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
from .data_type_parameter import ParameterDataType


class ResponseDataType(ParameterDataType):
    """
    The class for responses.
        This is essentially identical to a :class:`~.ParameterDataType`, however can be handled differently in the final
        application and thus exists as its own class/object.

    .. note:: When checking whether an object is a response or a parameter, note that
              :func:`isinstance(obj, ParameterDataType)` will also return true if the object is a
              :class:`ResponseDataType`, since they are derived from each other. Use ``type(obj) is ParameterDataType``
              for a precise check.
    """
