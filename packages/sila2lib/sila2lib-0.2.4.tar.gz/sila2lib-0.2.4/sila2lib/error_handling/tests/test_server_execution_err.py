# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import base64
import logging
import unittest
from unittest.mock import Mock
import grpc

# import the package modules/classes/exceptions
from ..server_err import SiLAError, SiLAExecutionError
#from ... import SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2


class TestValidationError(unittest.TestCase):

    def setUp(self) -> None:
        # deactivate logging during unittests
        logging.disable(level=logging.CRITICAL)

    def test_raise_undefined_execution_error(self):
        # try the default message
        try:
            raise SiLAExecutionError
        except SiLAExecutionError as err:
            self.assertIsNone(err.error_identifier)
            self.assertEqual(err.message,
                             'An undefined error has occurred while executing a server command or accessing a server '
                             'property.')
            self.assertIsInstance(err, SiLAError)
        # try a custom message
        try:
            raise SiLAExecutionError(msg='message')
        except SiLAExecutionError as err:
            self.assertIsNone(err.error_identifier)
            self.assertEqual(err.message, 'message')

    def test_raise_defined_execution_error(self):
        # try the default message
        try:
            raise SiLAExecutionError(error_identifier='err_id')
        except SiLAExecutionError as err:
            self.assertEqual(err.error_identifier, 'err_id')
            self.assertEqual(err.message,
                             'An error of type err_id has occurred during the execution of a command or while '
                             'accessing a property.')
            self.assertIsInstance(err, SiLAError)
        # try a custom message
        try:
            raise SiLAExecutionError(error_identifier='err_id', msg='message')
        except SiLAExecutionError as err:
            self.assertEqual(err.error_identifier, 'err_id')
            self.assertEqual(err.message, 'message')

    def test_get_error(self):
        # undefined
        try:
            raise SiLAExecutionError(msg='message')
        except SiLAExecutionError as err:
            error_message = err.get_error()
            self.assertIsInstance(error_message, silaFW_pb2.SiLAError)
            self.assertTrue(error_message.HasField('undefinedExecutionError'))
            self.assertEqual(error_message.undefinedExecutionError.message, 'message')
        # defined
        try:
            raise SiLAExecutionError(error_identifier='err_id', msg='message')
        except SiLAExecutionError as err:
            error_message = err.get_error()
            self.assertIsInstance(error_message, silaFW_pb2.SiLAError)
            self.assertTrue(error_message.HasField('definedExecutionError'))
            self.assertEqual(error_message.definedExecutionError.errorIdentifier, 'err_id')
            self.assertEqual(error_message.definedExecutionError.message, 'message')

    def test_raise_rpc_error_auto(self):
        # undefined
        try:
            raise SiLAExecutionError(msg='message')
        except SiLAExecutionError as err:
            context = Mock()
            err.raise_rpc_error(context=context)
            context.abort.assert_called_with(
                code=grpc.StatusCode.ABORTED,
                details=base64.b64encode(err.get_error().SerializeToString())
            )
        # defined
        try:
            raise SiLAExecutionError(error_identifier='err_id', msg='message')
        except SiLAExecutionError as err:
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
