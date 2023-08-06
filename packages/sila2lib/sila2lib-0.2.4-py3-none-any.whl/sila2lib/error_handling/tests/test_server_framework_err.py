# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import base64
import logging
import unittest
from unittest.mock import Mock
import grpc

# import the package modules/classes/exceptions
from ..server_err import SiLAError, SiLAFrameworkError, SiLAFrameworkErrorType
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
#from ... import SiLAFramework_pb2 as silaFW_pb2


class TestValidationError(unittest.TestCase):

    def setUp(self) -> None:
        # deactivate logging during unittests
        logging.disable(level=logging.CRITICAL)

    def test_raise(self):
        for error_type in SiLAFrameworkErrorType:
            # try the default message
            try:
                raise SiLAFrameworkError(error_type=error_type)
            except SiLAFrameworkError as err:
                self.assertEqual(err.framework_error_type, error_type)
                self.assertEqual(err.message,
                                 'A SiLA framework error of type {error_type} has occurred'.format(
                                     error_type=error_type.name
                                 ))
                self.assertIsInstance(err, SiLAError)
            # try a custom message
            try:
                raise SiLAFrameworkError(error_type=error_type, msg='message')
            except SiLAFrameworkError as err:
                self.assertEqual(err.framework_error_type, error_type)
                self.assertEqual(err.message, 'message')

    def test_get_error(self):
        for error_type in SiLAFrameworkErrorType:
            try:
                raise SiLAFrameworkError(error_type=error_type, msg='message')
            except SiLAFrameworkError as err:
                error_message = err.get_error()
                self.assertIsInstance(error_message, silaFW_pb2.SiLAError)
                self.assertTrue(error_message.HasField('frameworkError'))
                self.assertEqual(error_message.frameworkError.errorType, error_type)
                self.assertEqual(error_message.frameworkError.message, 'message')

    def test_raise_rpc_error_auto(self):
        for error_type in SiLAFrameworkErrorType:
            try:
                raise SiLAFrameworkError(error_type=error_type, msg='message')
            except SiLAFrameworkError as err:
                context = Mock()
                err.raise_rpc_error(context=context)
                context.abort.assert_called_with(
                    code=grpc.StatusCode.ABORTED,
                    #message=err.get_error().SerializeToString()
                    details=base64.b64encode(err.get_error().SerializeToString())
                )

    @unittest.skip("Manual error passing to err.raise_rpc_error() ignored.")
    def test_raise_rpc_error_manual(self):
        pass


if __name__ == '__main__':
    unittest.main()
