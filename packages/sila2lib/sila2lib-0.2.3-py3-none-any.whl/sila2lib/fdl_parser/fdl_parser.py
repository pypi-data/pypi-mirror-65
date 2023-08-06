"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: The main parser for FDL files that reads all sub-elements and constructs the object tree.

:file:    fdl_parser.py
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

# we need to supply a lot of information, so we consider this okay
# pylint: disable=too-many-instance-attributes

# import meta packages
from typing import Any, Dict

# import general packages
from lxml import etree, objectify

# load modules from this package
from .fdl_sila_reader import FDLSiLAReader
from .command import Command
from .property import Property
from .metadata import Metadata
from .data_type_definition import DataTypeDefinition
from .standard_errors import DefinedExecutionError


class FDLParser(FDLSiLAReader):
    """This class builds a tree of dictionaries that represent the feature defined in an FDL/XML input file."""

    # Basic access elements for the feature definition
    #: The filename for the feature that has been read
    fdl_filename: str

    #: The root of the XML input file
    root: Any

    # General information about this feature
    #: Identifier of the command
    identifier: str

    #: Display name property of the command
    name: str

    #: Command description
    description: str

    # Attributes of the feature definition
    #: The version of the SiLA2 protocol used in this feature definition file
    sila2_version: str

    #: Category of this feature (optional)
    category: str

    #: Maturity level (optional, default: Draft)
    maturity_level: str

    #: Language (optional, default: en-US)
    locale: str

    #: Originator, e.g. 'org.silastandard'
    originator: str

    #: The features version
    feature_version: str

    #: Major feature version for easy comparison
    feature_version_minor: int

    #: Minor feature version for easy comparison
    feature_version_major: int

    # Storage dictionaries for everything defined in this feature
    #: Dictionary of defined commands, the commands identifier is used as key
    commands: Dict[str, Command]

    #: Dictionary of defined properties, the properties identifier is used as a key
    properties: Dict[str, Property]

    #: Dictionary of all defined execution errors, the errors identifier is used as a key (SiLA v0.2)
    defined_execution_errors: Dict[str, DefinedExecutionError]

    #: Dictionary of data types defined, the data types identifier is used as a key
    data_type_definitions: Dict[str, DataTypeDefinition]

    def __init__(self, fdl_filename, fdl_schema_filename: str = None):
        """
        FDLParser class initialiser.

        :param fdl_filename: filename of FDL file to read.
        :param fdl_schema_filename: filename of the FDL scheme. If None, it will be set the the FDL scheme stored
                                    in this package.
        """
        super().__init__(fdl_schema_filename=fdl_schema_filename)

        self.fdl_filename = fdl_filename

        # create a parser and generate python object(s) from XML structure
        schema = etree.XMLSchema(file=self.fdl_schema_filename)
        parser = objectify.makeparser(schema=schema)
        tree = objectify.parse(self.fdl_filename, parser)

        # get access to the root element
        self.root = tree.getroot()

        # extract basic attributes
        #   mandatory elements
        self.sila2_version = str(self.root.get('SiLA2Version'))
        self.feature_version = str(self.root.get('FeatureVersion'))
        self.feature_version_major = int(self.feature_version.split('.')[0])
        self.feature_version_minor = int(self.feature_version.split('.')[1])
        self.originator = str(self.root.get('Originator'))
        # optional elements
        self.locale = str(self.root.get('Locale')) if 'Locale' in self.root.attrib else 'en-us'
        self.maturity_level = str(self.root.get('MaturityLevel')) if 'MaturityLevel' in self.root.attrib else 'Draft'
        self.category = str(self.root.get('Category')) if 'Category' in self.root.attrib else None

        # extract feature details
        self.identifier = self.root.Identifier.text
        self.name = self.root.DisplayName.text
        self.description = self.root.Description.text

        # Import definitions first, so they are (in theory) available later on
        #   Data type definitions
        self.data_type_definitions = {}
        if hasattr(self.root, 'DataTypeDefinition'):
            for data_type_definition in self.root.DataTypeDefinition:
                obj = DataTypeDefinition(xml_tree_element=data_type_definition)
                self.data_type_definitions[obj.identifier] = obj
        # Defined Execution Errors
        self.defined_execution_errors = {}
        if hasattr(self.root, 'DefinedExecutionError'):
            for defined_execution_error in self.root.DefinedExecutionError:
                obj = DefinedExecutionError(xml_tree_element=defined_execution_error)
                self.defined_execution_errors[obj.identifier] = obj
        # Import Server Commands, Properties, and Metadata
        self.commands = {}
        if hasattr(self.root, 'Command'):
            for xml_command in self.root.Command:
                obj = Command(xml_tree_element=xml_command)
                self.commands[obj.identifier] = obj
        self.properties = {}
        if hasattr(self.root, 'Property'):
            for xml_property in self.root.Property:
                obj = Property(xml_tree_element=xml_property)
                self.properties[obj.identifier] = obj
        self.metadata = {}
        if hasattr(self.root, 'Metadata'):
            for xml_metadata in self.root.Metadata:
                obj = Metadata(xml_tree_element=xml_metadata)
                self.metadata[obj.identifier] = obj
