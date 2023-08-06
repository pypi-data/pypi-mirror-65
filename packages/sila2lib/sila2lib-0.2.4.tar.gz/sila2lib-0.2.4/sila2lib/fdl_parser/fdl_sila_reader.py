"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Base class for reading SiLA FDL files.

:file:    fdl_sila_reader.py
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

# import general packages
import os
import logging


class FDLSiLAReader:
    """Base class to read SiLA FDL/XML files."""

    def __init__(self, fdl_schema_filename: str = None):
        """
        Class initialiser.

        :param fdl_schema_filename: The filename to the schema file which is used when parsing or validating an FDL
                                    file. If this is None, the default schema file from this library is loaded.
        """

        if fdl_schema_filename is None:
            self.fdl_schema_filename = os.path.join(os.path.dirname(__file__),
                                                    "..", "framework", "schema", "FeatureDefinition.xsd")
            logging.debug(
                'Set schema file for FDL/XML parsing to {schema_filename}'.format(
                    schema_filename=self.fdl_schema_filename
                )
            )
        else:
            self.fdl_schema_filename = fdl_schema_filename
