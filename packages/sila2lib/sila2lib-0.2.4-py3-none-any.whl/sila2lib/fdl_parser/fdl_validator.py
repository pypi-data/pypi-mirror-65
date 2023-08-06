"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Module used to validate FDL files for their validity based on the SiLA schemata.

:file:    fdl_validator.py
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

# Since the lxml library might raise arbitrary exceptions while reading/validating the input, we actually *want*
#   to catch 'em all
# pylint: disable=broad-except

# import general packages
import logging
from lxml import etree, objectify

# load modules from this package
from .fdl_sila_reader import FDLSiLAReader


class FDLValidator(FDLSiLAReader):
    """Validator a FDL/XML input file"""

    def __init__(self, fdl_schema_file: str = None):
        """
        Class initialiser

        :param fdl_schema_file: Path to the FDL schema file, if not given the FDL scheme supplied in this package
                                will be used.

        .. seealso:: The constructor of :class:`FDLSiLAReader` (:meth:`FDLSiLAReader.__init__`) is used to generate the
                     path to the schema file.s
        """
        super().__init__(fdl_schema_filename=fdl_schema_file)

    def validate(self, input_file: str) -> bool:
        """
        Validating Feature Definition FDL / XML according to SiLA2 schema

            :param input_file: File to validate with the given schema

            :returns: Whether the input file is valid based on the FDL schema file
        """
        logging.info("Validating FDL file {fdl_filename}".format(fdl_filename=input_file))
        try:
            schema = etree.XMLSchema(file=self.fdl_schema_filename)
            parser = objectify.makeparser(schema=schema)
            _ = objectify.parse(input_file, parser)
            is_valid = True

        except Exception as err:
            logging.error('An unknown error occurred while validating the input file ({input_file}): {error}'.format(
                input_file=input_file,
                error=err
            ))
            is_valid = False

        return is_valid
