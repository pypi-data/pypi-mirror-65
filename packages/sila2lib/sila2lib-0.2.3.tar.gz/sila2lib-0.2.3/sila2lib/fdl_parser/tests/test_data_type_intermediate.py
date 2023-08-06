# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..data_type_parameter import ParameterDataType
from ..data_type_intermediate import IntermediateDataType


class TestResponseDataType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.

        *Nothing to set up.*
        """

    def test_intermediate_data_type_object(self):
        """
        Check whether we can identify a IntermediateDataType.
            A nIntermediateDataType object is effectively identical to a ParameterResponseType object. So we have only
            one way to distinguish them, which we test here and now.
        """
        from ._data_data_type_parameter import DATA_BASIC
        obj = IntermediateDataType(objectify.fromstring(DATA_BASIC).Parameter)

        self.assertIs(type(obj), IntermediateDataType)
        self.assertIsNot(type(obj), ParameterDataType)
