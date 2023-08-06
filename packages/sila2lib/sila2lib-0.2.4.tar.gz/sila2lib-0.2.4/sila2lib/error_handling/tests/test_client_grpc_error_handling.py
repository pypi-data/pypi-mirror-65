# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import base64
import logging
import unittest
from unittest.mock import Mock

# import the package modules/classes/exceptions
from ..client_err import grpc_error_handling, SiLAError
#from .. import SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2


class TestGrpcErrorHandling(unittest.TestCase):

    def setUp(self):
        # deactivate logging during unittests
        logging.disable(level=logging.CRITICAL)

    def test_validation_error(self):
        # create an grpc.Call-like error object
        error_object = Mock()
        error_object.code.return_value = '42'

        sila_error = silaFW_pb2.SiLAError(
            validationError=silaFW_pb2.ValidationError(
                parameter='parameter',
                message='message'
            )
        )
        ser_message = sila_error.SerializeToString()
        error_object.details.return_value = base64.b64encode(ser_message)

        # parse the thingy
        error_result = grpc_error_handling(error_object=error_object)

        self.assertEqual(error_result.error_type, SiLAError.VALIDATION_ERROR)
        self.assertEqual(error_result.message, sila_error.validationError)

    def test_framework_error(self):
        # create an grpc.Call-like error object
        error_object = Mock()
        error_object.code.return_value = '42'

        sila_error = silaFW_pb2.SiLAError(
            frameworkError=silaFW_pb2.FrameworkError(
                errorType=42,
                message='message'
            )
        )
        # error_object.details.return_value = sila_error.SerializeToString()
        ser_message = sila_error.SerializeToString()
        error_object.details.return_value = base64.b64encode(ser_message)

        # parse the thingy
        error_result = grpc_error_handling(error_object=error_object)

        self.assertEqual(error_result.error_type, SiLAError.FRAMEWORK_ERROR)
        self.assertEqual(error_result.message, sila_error.frameworkError)

    def test_defined_execution_error(self):
        # create an grpc.Call-like error object
        error_object = Mock()
        error_object.code.return_value = '42'

        sila_error = silaFW_pb2.SiLAError(
                definedExecutionError=silaFW_pb2.DefinedExecutionError(
                errorIdentifier='error_id',
                message='message'
            )
        )
        #error_object.details.return_value = sila_error.SerializeToString()
        ser_message = sila_error.SerializeToString()
        error_object.details.return_value = base64.b64encode(ser_message)

        # parse the thingy
        error_result = grpc_error_handling(error_object=error_object)

        self.assertEqual(error_result.error_type, SiLAError.DEFINED_EXECUTION_ERROR)
        self.assertEqual(error_result.message, sila_error.definedExecutionError)

    def test_undefined_execution_error(self):
        # create an grpc.Call-like error object
        error_object = Mock()
        error_object.code.return_value = '42'

        sila_error = silaFW_pb2.SiLAError(
                undefinedExecutionError=silaFW_pb2.UndefinedExecutionError(
                message='message'
            )
        )
        #error_object.details.return_value = sila_error.SerializeToString()
        ser_message = sila_error.SerializeToString()
        error_object.details.return_value = base64.b64encode(ser_message)

        # parse the thingy
        error_result = grpc_error_handling(error_object=error_object)

        self.assertEqual(error_result.error_type, SiLAError.UNDEFINED_EXECUTION_ERROR)
        self.assertEqual(error_result.message, sila_error.undefinedExecutionError)

    def test_no_sila_error(self):
        # create an grpc.Call-like error object
        error_object = Mock()
        error_object.code.return_value = '42'
        error_object.details.return_value = base64.b64encode('no_sila_message'.encode('utf-8'))

        error_result = grpc_error_handling(error_object=error_object)
        self.assertIsNone(error_result)

    @unittest.skip('I really do not know how to test this. Apart from that, unknown SiLA errors should not occur '
                   'anyway...')
    def test_unknown_sila_error(self):
        pass
