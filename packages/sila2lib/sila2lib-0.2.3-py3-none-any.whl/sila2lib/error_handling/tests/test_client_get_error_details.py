# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import logging
import unittest
from unittest.mock import Mock, PropertyMock

# import the package modules/classes/exceptions
from ..client_err import get_validation_error_details, \
    get_framework_error_details, \
    get_defined_execution_error_details, \
    get_undefined_execution_error_details

#from ... import SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

class TestGetErrorDetails(unittest.TestCase):

    def setUp(self) -> None:
        """nothing to do here."""
        pass

    def test_validation_error(self):
        message = Mock()
        type(message).parameter = PropertyMock(return_value='the_parameter')
        type(message).message = PropertyMock(return_value='the_message')

        details = get_validation_error_details(message=message)

        self.assertEqual(details, 'Message: the_message; Parameter: the_parameter')

    def test_framework_error(self):
        message = Mock()
        type(message).errorType = PropertyMock(return_value='the_error_type')
        type(message).message = PropertyMock(return_value='the_message')

        details = get_framework_error_details(message=message)

        self.assertEqual(details, 'Error Type: the_error_type; Message: the_message')

    def test_defined_execution_error(self):
        message = Mock()
        type(message).errorIdentifier = PropertyMock(return_value='the_error_identifier')
        type(message).message = PropertyMock(return_value='the_message')

        details = get_defined_execution_error_details(message=message)

        self.assertEqual(details, 'Error Identifier: the_error_identifier; Message: the_message')

    def test_undefined_execution_error(self):
        message = Mock()
        type(message).message = PropertyMock(return_value='the_message')

        details = get_undefined_execution_error_details(message=message)

        self.assertEqual(details, 'Message: the_message')
