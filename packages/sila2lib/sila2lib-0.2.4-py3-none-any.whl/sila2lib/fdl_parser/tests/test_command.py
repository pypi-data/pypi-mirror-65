# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access

# import general Packages
import unittest
import logging
from lxml import objectify

# import package related modules and classes
from ..command import Command
from ..data_type_parameter import ParameterDataType
from ..data_type_response import ResponseDataType
from ..data_type_intermediate import IntermediateDataType
from ..type_basic import BasicType


class TestCommand(unittest.TestCase):

    def setUp(self):
        # deactivate logging during unittests
        logging.disable(level=logging.CRITICAL)

    def test_tree(self):
        from ._data_command import DATA_SIMPLE

        xml_input = objectify.fromstring(DATA_SIMPLE).Command
        obj = Command(xml_tree_element=xml_input)

        self.assertEqual(xml_input, obj._tree)

    def test_attributes(self):
        from ._data_command import DATA_SIMPLE

        obj = Command(xml_tree_element=objectify.fromstring(DATA_SIMPLE).Command)
        # check simple attributes
        self.assertEqual(
            obj.identifier,
            "CommandIdentifier"
        )
        self.assertEqual(
            obj.name,
            "Command Name"
        )
        self.assertEqual(
            obj.description,
            "Simple, unobservable command without any complex elements"
        )
        self.assertFalse(obj.observable)
        # check parameter and responses
        self.assertEqual(len(obj.parameters), 1)
        self.assertEqual(len(obj.responses), 1)
        self.assertIn('ParameterIdentifier', obj.parameters)
        self.assertIn('ResponseIdentifier', obj.responses)
        self.assertIs(type(obj.parameters['ParameterIdentifier']), ParameterDataType)
        self.assertIs(type(obj.responses['ResponseIdentifier']), ResponseDataType)

    def test_observable(self):
        from ._data_command import DATA_OBSERVABLE

        obj = Command(xml_tree_element=objectify.fromstring(DATA_OBSERVABLE).Command)
        self.assertTrue(obj.observable)

    def test_parameter(self):
        from ._data_command import DATA_EMPTY_PARAMETER, DATA_EMPTY_BOTH, DATA_MULTIPLE_PARAMETER

        with self.subTest(parameter="empty_parameter"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_EMPTY_PARAMETER).Command)

            self.assertEqual(len(obj.parameters), 1)
            self.assertEqual(len(obj.responses), 1)
            self.assertIn('EmptyParameter', obj.parameters)
            self.assertIs(type(obj.parameters['EmptyParameter']), ParameterDataType)
            self.assertIs(type(obj.parameters['EmptyParameter'].sub_type), BasicType)
            self.assertEqual(
                obj.parameters['EmptyParameter'].sub_type.sub_type,
                'Void'
            )
        with self.subTest(parameter="empty_both"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_EMPTY_BOTH).Command)

            self.assertEqual(len(obj.parameters), 1)
            self.assertEqual(len(obj.responses), 1)
            self.assertIn('EmptyParameter', obj.parameters)
            self.assertIs(type(obj.parameters['EmptyParameter']), ParameterDataType)
            self.assertIs(type(obj.parameters['EmptyParameter'].sub_type), BasicType)
            self.assertEqual(
                obj.parameters['EmptyParameter'].sub_type.sub_type,
                'Void'
            )
        with self.subTest(parameter="multiple"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_MULTIPLE_PARAMETER).Command)

            self.assertEqual(len(obj.parameters), 3)
            self.assertEqual(len(obj.responses), 1)
            for index in range(1, 3):
                identifier = 'ParameterIdentifier{index}'.format(index=index)
                self.assertIn(identifier, obj.parameters)
                self.assertIs(type(obj.parameters[identifier]), ParameterDataType)

    def test_responses(self):
        from ._data_command import DATA_EMPTY_RESPONSE, DATA_EMPTY_BOTH, DATA_MULTIPLE_RESPONSES

        with self.subTest(parameter="empty_response"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_EMPTY_RESPONSE).Command)

            self.assertEqual(len(obj.parameters), 1)
            self.assertEqual(len(obj.responses), 1)
            self.assertIn('EmptyResponse', obj.responses)
            self.assertIs(type(obj.responses['EmptyResponse']), ResponseDataType)
            self.assertIs(type(obj.responses['EmptyResponse'].sub_type), BasicType)
            self.assertEqual(
                obj.responses['EmptyResponse'].sub_type.sub_type,
                'Void'
            )
        with self.subTest(parameter="empty_both"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_EMPTY_BOTH).Command)

            self.assertEqual(len(obj.parameters), 1)
            self.assertEqual(len(obj.responses), 1)
            self.assertIn('EmptyResponse', obj.responses)
            self.assertIs(type(obj.responses['EmptyResponse']), ResponseDataType)
            self.assertIs(type(obj.responses['EmptyResponse'].sub_type), BasicType)
            self.assertEqual(
                obj.responses['EmptyResponse'].sub_type.sub_type,
                'Void'
            )
        with self.subTest(parameter="multiple"):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_MULTIPLE_RESPONSES).Command)

            self.assertEqual(len(obj.parameters), 1)
            self.assertEqual(len(obj.responses), 3)
            for index in range(1, 3):
                identifier = 'ResponseIdentifier{index}'.format(index=index)
                self.assertIn(identifier, obj.responses)
                self.assertIs(type(obj.responses[identifier]), ResponseDataType)

    def test_intermediate_responses(self):
        from ._data_command import DATA_OBSERVABLE, DATA_OBSERVABLE_INTERMEDIATE, DATA_UNOBSERVABLE_INTERMEDIATE

        with self.subTest(observeable="Yes", intermediate=False):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_OBSERVABLE).Command)

            self.assertEqual(len(obj.intermediates), 0)

        with self.subTest(observeable="Yes", intermediate=True):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_OBSERVABLE_INTERMEDIATE).Command)

            self.assertEqual(len(obj.intermediates), 1)
            self.assertIn('IntermediateIdentifier', obj.intermediates)
            self.assertIs(type(obj.intermediates['IntermediateIdentifier']), IntermediateDataType)
            self.assertEqual(
                obj.intermediates['IntermediateIdentifier'].identifier,
                'IntermediateIdentifier'
            )
            self.assertEqual(
                obj.intermediates['IntermediateIdentifier'].description,
                'A random intermediate response definition.'
            )
            self.assertEqual(
                obj.intermediates['IntermediateIdentifier'].name,
                'Intermediate Identifier'
            )

        with self.subTest(observeable="No", intermediate=True):
            obj = Command(xml_tree_element=objectify.fromstring(DATA_UNOBSERVABLE_INTERMEDIATE).Command)

            self.assertEqual(len(obj.intermediates), 0)

    def test_defined_execution_errors(self):
        from ._data_command import DATA_DEFINED_EXECUTION_ERRORS

        obj = Command(xml_tree_element=objectify.fromstring(DATA_DEFINED_EXECUTION_ERRORS).Command)

        self.assertEqual(len(obj.defined_execution_errors), 3)
        for index in range(1, 3):
            identifier = "ExecutionError{index}".format(index=index)
            self.assertIn(identifier, obj.defined_execution_errors)


if __name__ == '__main__':
    unittest.main()
