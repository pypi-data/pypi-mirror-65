"""
__________________________________________________________________________________________________

:project: SiLA2_python

:details: Command element in a SiLA Feature Definition.

:file:    command.py
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

# we need to distinguish all the sub-elements, so allow the branches
# pylint: disable=too-many-branches, too-many-instance-attributes

# import meta packages
from typing import Any
from typing import Dict, List

# import general packages
import logging
from lxml import objectify

# import library packages
from .data_type_parameter import ParameterDataType
from .data_type_response import ResponseDataType
from .data_type_intermediate import IntermediateDataType


class Command:
    """
    This class stores all information corresponding to **one** command defined in the feature definition.
    """

    #: Identifier of the command
    identifier: str

    #: Display name property of the command
    name: str

    #: Command description
    description: str

    #: Is this an observable command
    observable: bool

    #: Reference to the xml-tree of the command
    _tree: Any

    #: Dictionary of parameters that are defined for this command
    parameters: Dict[str, ParameterDataType]

    #: Dictionary of responses that are defined for this command
    responses: Dict[str, ResponseDataType]

    #: Dictionary for Intermediate Responses (not yet implemented)
    intermediates: Dict[str, IntermediateDataType]

    #: List of all defined execution errors (identifiers) that can occur during this command (SiLA v0.2)
    defined_execution_errors: List[str]

    def __init__(self, xml_tree_element):
        """
        Class initialiser

        :param xml_tree_element: The contents of the <Command>-xml node
        """
        self._tree = xml_tree_element

        self.identifier = xml_tree_element.Identifier.text
        self.name = xml_tree_element.DisplayName
        self.description = xml_tree_element.Description

        self.observable = xml_tree_element.Observable.text.lower() == 'yes'

        # get all parameters
        self.parameters = {}
        if hasattr(xml_tree_element, 'Parameter'):
            for parameter in xml_tree_element.Parameter:
                obj = ParameterDataType(xml_tree_element=parameter)
                self.parameters[obj.identifier] = obj
        else:
            logging.debug('No parameter found for command {command_id}. Adding empty parameter.'.format(
                command_id=self.identifier
            ))
            obj = ParameterDataType(xml_tree_element=self.genParmeterVoidXMLTree())
            self.parameters[obj.identifier] = obj

        # get all responses
        self.responses = {}
        if hasattr(xml_tree_element, 'Response'):
            for response in xml_tree_element.Response:
                obj = ResponseDataType(xml_tree_element=response)
                self.responses[obj.identifier] = obj
        else:
            logging.debug('No response found for command {command_id}. Adding empty response.'.format(
                command_id=self.identifier
            ))
            obj = ResponseDataType(xml_tree_element=self.genResponseVoidXMLTree())
            self.responses[obj.identifier] = obj

        # get all intermediate responses
        self.intermediates = {}
        if hasattr(xml_tree_element, 'IntermediateResponse'):
            if self.observable:
                for intermediate in xml_tree_element.IntermediateResponse:
                    obj = IntermediateDataType(xml_tree_element=intermediate)
                    self.intermediates[obj.identifier] = obj
            else:
                logging.error(
                    (
                        'Command {command_id} is not observable but has intermediate responses defined. '
                        'This is invalid, we are going to ignore the intermediates.'
                    ).format(command_id=self.identifier)
                )
        else:
            pass

        # get all execution errors
        self.defined_execution_errors = []
        if hasattr(xml_tree_element, 'DefinedExecutionErrors'):
            for defined_error in xml_tree_element.DefinedExecutionErrors.Identifier:
                self.defined_execution_errors.append(defined_error.text)

    def genParmeterVoidXMLTree(self):
        """
        Define the XML-tree from which the empty parameter is constructed if a command has no parameters
        Note that the identifier is as important as the text, since it will be used as dictionary key for access
        """
        E = objectify.ElementMaker(annotate=False)  # lxml E-factory
        parameter_void = E.Parameter( E.Identifier('EmptyParameter'),
                                      E.DisplayName('Empty Parameter'),
                                      E.Description('An empty parameter data type used if no parameter is required.'),
                                      E.DataType(
                                         E.Basic('Void'),
                                      )
                                     )
        return parameter_void

    def genResponseVoidXMLTree(self):
        """
        Define the xml-tree from which the empty response is constructed if a command has no responses
        Note that the identifier is as important as the text, since it will be used as dictionary key for access
        """
        E = objectify.ElementMaker(annotate=False)  # lxml E-factory
        response_void = E.Parameter( E.Identifier('EmptyResponse'),
                                     E.DisplayName('Empty Response'),
                                     E.Description('An empty response data type used if no response is required.'),
                                     E.DataType(
                                         E.Basic('Void'),
                                     )
                                   )
        return response_void
