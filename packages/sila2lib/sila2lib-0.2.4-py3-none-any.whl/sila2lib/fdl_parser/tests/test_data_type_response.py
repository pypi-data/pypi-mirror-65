# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..data_type_parameter import ParameterDataType
from ..data_type_response import ResponseDataType


class TestResponseDataType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_response_data_type_object(self):
        """
        Check whether we can identify a ResponseDataType.
            A ResponseDataType object is effectively identical to a ParameterResponseType object. So we have only one
            way to distinguish them, which we test here and now.
        """
        from ._data_data_type_parameter import DATA_BASIC
        obj = ResponseDataType(objectify.fromstring(DATA_BASIC).Parameter)

        self.assertIs(type(obj), ResponseDataType)
        self.assertIsNot(type(obj), ParameterDataType)
