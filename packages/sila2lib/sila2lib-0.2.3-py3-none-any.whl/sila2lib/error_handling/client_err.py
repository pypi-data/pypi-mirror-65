"""
________________________________________________________________________

:PROJECT: SiLA2_python

:details: SiLA2 client error handling.

:file:    client_err.py
:authors: Timm Severin

:date: (creation)          20190806
:date: (last modification) 20190823

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

# import meta classes
from typing import Union, Optional
from typing import NamedTuple

# import general packages
from enum import Enum
import grpc
import base64
from google.protobuf.message import DecodeError as grpcDecodeError

# import package contents
from ..framework import SiLAFramework_pb2 as silaFW_pb2


class SiLAError(Enum):
    """
    Enumeration for all different SiLA error types.
    """
    VALIDATION_ERROR = 'validationError'
    FRAMEWORK_ERROR = 'frameworkError'
    DEFINED_EXECUTION_ERROR = 'definedExecutionError'
    UNDEFINED_EXECUTION_ERROR = 'undefinedExecutionError'
    UNKNOWN = 'unknown'


class GrpcError(NamedTuple):
    """
    NamedTuple for the return value of the :func:`grpc_error_handling` function that specifies the error type and the
    actual message.
    """
    error_type: SiLAError
    message: Union[silaFW_pb2.ValidationError,
                   silaFW_pb2.FrameworkError,
                   silaFW_pb2.DefinedExecutionError,
                   silaFW_pb2.UndefinedExecutionError]


def grpc_error_handling(error_object: grpc.Call) -> Optional[GrpcError]:
    """
    Handles exceptions of type grpc.RpcError
        This function parses a gRPC error that occurred during the communication with a server and extracts the
        corresponding `SiLAError`.

    :returns: The type of the error if it is a SiLA error or None otherwise. If the message could be evaluated as
              SiLAError, but the type could not be identified, the return value will include the SiLAError message
              itself, otherwise the specific error `SiLAFramework_pb2.ValidationError`, ... will be passed.
    """

    try:
        message = silaFW_pb2.SiLAError()
        if use_base64_encoding:
            message.ParseFromString(base64.b64decode(error_object.details()))
        else:
            message.ParseFromString(bytes(error_object.details(), 'utf-8'))
    except grpcDecodeError:
        # not a SiLA error, just output the details
        logging.exception(
            (
                'Error during gRPC communication. (No SiLA 2 Error !) ' '\n'
                '\t' 'Status code: {error_code}' '\n'
                '\t' 'Details: {error_details}' '\n ---- end gRPC err -----\n'

            ).format(
                error_code=error_object.code(),
                error_details=base64.b64decode(error_object.details()) #error_object.details()
            )
        )
        return None

    if message.HasField('validationError'):
        details = get_validation_error_details(message=message.validationError)
        return_value = GrpcError(
            error_type=SiLAError.VALIDATION_ERROR,
            message=message.validationError)
    elif message.HasField('frameworkError'):
        details = get_framework_error_details(message=message.frameworkError)
        return_value = GrpcError(
            error_type=SiLAError.FRAMEWORK_ERROR,
            message=message.frameworkError)
    elif message.HasField('definedExecutionError'):
        details = get_defined_execution_error_details(message=message.definedExecutionError)
        return_value = GrpcError(
            error_type=SiLAError.DEFINED_EXECUTION_ERROR,
            message=message.definedExecutionError)
    elif message.HasField('undefinedExecutionError'):
        details = get_undefined_execution_error_details(message=message.undefinedExecutionError)
        return_value = GrpcError(
            error_type=SiLAError.UNDEFINED_EXECUTION_ERROR,
            message=message.undefinedExecutionError)
    else:
        details = 'Could not load details about the error, error type is unknown.'
        return_value = GrpcError(error_type=SiLAError.UNKNOWN, message=message)

    logging.exception(
        (
            'Error during gRPC communication.' '\n'
            '\t' 'Error type: {error_type}' '\n'
            '\t' 'Status code: {error_code}' '\n'
            '\t' 'Details: {error_details}' '\n'

        ).format(
            error_type=return_value.error_type.value,
            error_code=error_object.code(),
            error_details=details
        )
    )

    return return_value


def get_validation_error_details(message: silaFW_pb2.ValidationError) -> str:
    """
    Returns a string with the details send about the validation error.

    :param message: The ValidationError message as defined in the SiLA framework.

    :return: A descriptive string with all details stored.
    """

    return (
        'Message: {message}; '
        'Parameter: {parameter}'
    ).format(
        parameter=message.parameter,
        message=message.message
    )


def get_framework_error_details(message: silaFW_pb2.FrameworkError) -> str:
    """
    Returns a string with the details send about the framework error.

    :param message: The FrameworkError message as defined in the SiLA framework.

    :return: A descriptive string with all details stored.
    """

    return (
        'Error Type: {error_type}; '
        'Message: {message}'
    ).format(
        error_type=message.errorType,
        message=message.message
    )


def get_defined_execution_error_details(message: silaFW_pb2.DefinedExecutionError) -> str:
    """
    Returns a string with the details send about the defined execution error.

    :param message: The DefinedExecutionError message as defined in the SiLA framework.

    :return: A descriptive string with all details stored.

    .. note:: This error type was used starting in SiLA standard version 0.2
    """

    return (
        'Error Identifier: {error_identifier}; '
        'Message: {message}'
    ).format(
        error_identifier=message.errorIdentifier,
        message=message.message
    )


def get_undefined_execution_error_details(message: silaFW_pb2.UndefinedExecutionError) -> str:
    """
    Returns a string with the details send about the undefined execution error.

    :param message: The UndefinedExecutionError message as defined in the SiLA framework.

    :return: A descriptive string with all details stored.

    .. note:: This error type was used starting in SiLA standard version 0.2
    """

    return (
        'Message: {message}'
    ).format(
        message=message.message
    )
