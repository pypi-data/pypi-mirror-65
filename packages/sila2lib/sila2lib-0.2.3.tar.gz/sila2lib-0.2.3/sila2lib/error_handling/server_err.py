"""
________________________________________________________________________

:PROJECT: SiLA2_python

:details: SiLA2 server error handling.

:file:    server_err.py
:authors: Mark Doerr
          Florian Meinicke
          Timm Severin

:date: (creation)          20181223
:date: (last modification) 2019-09-18

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.2.0"

# Import the VIP
import logging

# import package options
from . import use_base64_encoding

# import meta packages
from abc import abstractmethod, ABC
from typing import Optional

# import packages for the execution
from enum import IntEnum
import base64
import grpc

# import package contents
from ..framework import SiLAFramework_pb2 as silaFW_pb2


class SiLAFrameworkErrorType(IntEnum):
    """Possible error types for SiLA2 FrameworkErrors."""
    #: The server does not allow the execution of this command
    COMMAND_EXECUTION_NOT_ACCEPTED = 0
    #: The given UUID for the observable subscription or property is invalid
    INVALID_COMMAND_EXECUTION_UUID = 1
    #: Trying to get a result of an observable command that is not (yet) finished
    COMMAND_EXECUTION_NOT_FINISHED = 2
    #: Required metadata has not been sent or has been sent using the wrong data type
    INVALID_METADATA = 3
    #: Metadata was sent, but no metadata is allowed by the server
    NO_METADATA_ALLOWED = 4


class SiLAError(Exception, ABC):
    """
    Base class for all SiLA related errors.
        This class can be used to catch all SiLA related errors. All further errors in a SiLA module should be
        derived from this one.
        This exception is *not* meant to be used to actually raise an error. since it can not be represented in the
        SiLA error model.
    """

    #: Message to be printed when the error is raised
    message: str

    @abstractmethod
    def __init__(self, msg: str = None):
        """
        Class initialiser.

        :param msg: Error message to associate with this exception. If None is given, an extremely generic error message
                    will be printed.

        ..note:: This method is defined as abstract, since it only provides a not helpful error message. In a best
                 case scenario, it should only be used to pass on the actual error message to the BaseException class.
        """
        # make sure we at least get a most generic error message
        if msg is None:
            msg = "An error occurred while running a SiLA related evaluation."
        # store the inputs
        self.message = msg
        super().__init__(msg)

    @abstractmethod
    def get_error(self) -> silaFW_pb2.SiLAError:
        """
        Method that must be implemented by the subclasses to produce the :class:`SiLAError` that is used

        :return: Returns a SiLAError object that can be sent to the client.
        """
        raise NotImplementedError

    def raise_rpc_error(self, context: grpc.ServicerContext, error: silaFW_pb2.SiLAError = None):
        """
        Raises the given error using the underlying gRPC framework.

        :param context: gRPC servicer context to modify for the error.
        :param error: The SiLA error object to be returned to the client. If omitted it will automatically be created
                      from the error object.
        """
        # if error is not given the subclass should implement the get_error() method which constructs the error
        if error is None:
            error = self.get_error()

        message = error.SerializeToString()
        if use_base64_encoding:
            message = base64.b64encode(message)

        logging.error('{error_type}: {message}'.format(
            error_type=self.__class__.__name__,
            message=self.message
        ))

        context.abort(
            code=grpc.StatusCode.ABORTED,
            details=message
        )

class SiLAValidationError(SiLAError):
    """
    Base class for any validation errors that occur in a SiLA module.
        A validation error is an error that occurs during the validation of parameters before executing a command.
    """

    #: The name of the parameter for which the validation failed
    parameter: str

    def __init__(self, parameter: str, msg: str = None):
        """
        Initialiser of the exception.

        :param parameter: The parameter for which the validation failed.
        :param msg: The error message to print. If left empty, a default validation error message will be used which
                    includes the parameter name. If set manually, the parameter name will *not* be included
                    automatically!
        """
        # set the message
        if msg is None:
            msg = "A validation error occurred during the evaluation of the function parameter {parameter}.".format(
                parameter=parameter
            )
        # store the data for later access
        self.parameter = parameter
        # call the base constructors
        super().__init__(msg)

    def get_error(self) -> silaFW_pb2.SiLAError:
        """
        Construct an object for a validation error.
        """
        return silaFW_pb2.SiLAError(
            validationError=silaFW_pb2.ValidationError(
                parameter=self.parameter,
                message=self.message
            )
        )


class SiLAExecutionError(SiLAError):
    """
    Base class for SiLA Execution Errors as defined in SiLA standard version 1.0.
        Is raised when during the execution of a command or the accessing of a property an error occurs.
        An Execution Error is an Error, which occurs during Command execution, a property access or an Error that is
        related to the use of SiLA Client Metadata.
        SiLA distinguishes between defined and undefined exection errors.
    """

    #: The identifier of the error as specified in the FDL/XML file for the feature. Can be left empty to indicate an
    #:  undefined execution error
    error_identifier: Optional[str]

    def __init__(self, error_identifier: str = None, msg: str = None):
        """
        Class initialiser for execution errors.
            This methods initialises both defined and undefined execution errors. The type is distinguished by the
             existence if the `error_identifier` parameter.

        :param error_identifier: If set to None, it is assumed that an undefined execution error occurred. Otherwise
                                 this parameter has to be set to a valid string for a defined execution error.
        :param msg: The error message. If not given or None, the message will be set to a generic default message,
                    which - in the case of a defined execution error - will automatically contain the error identifier.
                    Whens et manually, the error identifier will not be added automatically.
        """

        # set the default message based on the information supplied
        if msg is None:
            if error_identifier is not None:
                msg = 'An error of type {error_identifier} has occurred during the execution of a command or ' \
                      'while accessing a property.'.format(error_identifier=error_identifier)
            else:
                msg = 'An undefined error has occurred while executing a server command or accessing a server property.'
        # store the input
        self.error_identifier = error_identifier
        # call the base constructor
        super().__init__(msg)

    def get_error(self) -> silaFW_pb2.SiLAError:
        """
        Construct an object for an execution error.
        """

        if self.error_identifier is not None:
            sila_error = silaFW_pb2.SiLAError(
                definedExecutionError=silaFW_pb2.DefinedExecutionError(
                    errorIdentifier=self.error_identifier,
                    message=self.message
                )
            )
        else:
            sila_error = silaFW_pb2.SiLAError(
                undefinedExecutionError=silaFW_pb2.UndefinedExecutionError(
                    message=self.message
                )
            )

        return sila_error


class SiLAFrameworkError(SiLAError):
    """
    Base class for SiLA Framework errors.
        A Framework Error occurs when a client accesses a SiLA server in a way that violates the SiLA2 specification.
    """

    #: The type of the framework error based in the defined types in the SiLA specifications
    framework_error_type: SiLAFrameworkErrorType

    def __init__(self, error_type: SiLAFrameworkErrorType, msg: str = None):
        """
        Class initialiser.

        :param error_type: Type of the error that has occurred as defined in the SiLA Standard for framework errors.
        :param msg: The error message associated with the error. If omitted, a generic default message will be generated
                    which includes the name of the error_type. If set manually, the type of the error must be added
                    in the message.
        """
        # construct a generic default message
        if msg is None:
            msg = "A SiLA framework error of type {error_type} has occurred".format(
                error_type=error_type.name
            )
        # store inputs
        self.framework_error_type = error_type
        # base constructor
        super().__init__(msg)

    def get_error(self) -> silaFW_pb2.SiLAError:
        """
        Construct an object for a SiLA framework error
        """

        return silaFW_pb2.SiLAError(
            frameworkError=silaFW_pb2.FrameworkError(
                errorType=int(self.framework_error_type),
                message=self.message
            )
        )
