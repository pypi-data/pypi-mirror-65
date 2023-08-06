# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import base64
import logging
import unittest
from unittest.mock import Mock
import grpc

# import the package modules/classes/exceptions
from ..server_err import SiLAError, SiLAValidationError
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
#from ... import SiLAFramework_pb2 as silaFW_pb2


class TestValidationError(unittest.TestCase):

    def setUp(self) -> None:
        # deactivate logging during unittests
        logging.disable(level=logging.CRITICAL)

    def test_raise(self):
        # try the default message
        try:
            raise SiLAValidationError(parameter='parameter_name')
        except SiLAValidationError as err:
            self.assertEqual(err.parameter, 'parameter_name')
            self.assertEqual(err.message,
                             'A validation error occurred during the evaluation of the function parameter '
                             'parameter_name.')
            self.assertIsInstance(err, SiLAError)
        # try a custom message
        try:
            raise SiLAValidationError(parameter='parameter_name', msg='message')
        except SiLAValidationError as err:
            self.assertEqual(err.parameter, 'parameter_name')
            self.assertEqual(err.message, 'message')

    def test_get_error(self):
        try:
            raise SiLAValidationError(parameter='parameter_name', msg='message')
        except SiLAValidationError as err:
            error_message = err.get_error()
            self.assertIsInstance(error_message, silaFW_pb2.SiLAError)
            self.assertTrue(error_message.HasField('validationError'))
            self.assertEqual(error_message.validationError.parameter, 'parameter_name')
            self.assertEqual(error_message.validationError.message, 'message')

    def test_raise_rpc_error_auto(self):
        try:
            raise SiLAValidationError(parameter='parameter_name', msg='message')
        except SiLAValidationError as err:
            context = Mock()
            err.raise_rpc_error(context=context)
            context.abort.assert_called_with(
                code=grpc.StatusCode.ABORTED,
                details=base64.b64encode(err.get_error().SerializeToString())
            )

    @unittest.skip("Manual error passing to err.raise_rpc_error() ignored.")
    def test_raise_rpc_error_manual(self):
        pass


if __name__ == '__main__':
    unittest.main()
