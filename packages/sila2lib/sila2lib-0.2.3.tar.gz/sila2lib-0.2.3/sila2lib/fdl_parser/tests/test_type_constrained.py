# Set pylint configuration for this file
# pylint: disable=missing-docstring, protected-access, too-many-locals

# import general Packages
import unittest
from lxml import objectify

# import package related modules and classes
from ..type_constrained import ConstrainedType
from ..type_list import ListType
from ..type_basic import BasicType
from ..type_data_type_identifier import DataTypeIdentifier

# import custom exceptions
from ..exceptions.exceptions import SubDataTypeError, ConstraintTypeWarning, ConstraintValueWarning, \
    ConstraintUnsupportedContentType


class TestConstrainedType(unittest.TestCase):

    def setUp(self):
        """
        Sets up basic attributes for the unit tests run in this class.
            Loads all constraint strings so they can be used more easily later.
        """
        from ._data_type_constrained import DATA_CONSTRAINT_LENGTH, DATA_CONSTRAINT_LENGTH_MINIMAL, \
            DATA_CONSTRAINT_LENGTH_MAXIMAL, DATA_CONSTRAINT_SET, DATA_CONSTRAINT_PATTERN, \
            DATA_CONSTRAINT_VALUE_MAXIMAL_EXCLUSIVE, DATA_CONSTRAINT_VALUE_MAXIMAL_INCLUSIVE, \
            DATA_CONSTRAINT_VALUE_MINIMAL_EXCLUSIVE, DATA_CONSTRAINT_VALUE_MINIMAL_INCLUSIVE, \
            DATA_CONSTRAINT_ELEMENTS_COUNT, DATA_CONSTRAINT_ELEMENTS_MINIMAL, DATA_CONSTRAINT_ELEMENTS_MAXIMAL, \
            DATA_CONSTRAINT_UNIT, DATA_CONSTRAINT_CONTENT_TYPE, DATA_CONSTRAINT_IDENTIFIER, DATA_CONSTRAINT_SCHEMA
        self.constraints_basic = {
            'Length':                   DATA_CONSTRAINT_LENGTH,
            'MinimalLength':            DATA_CONSTRAINT_LENGTH_MINIMAL,
            'MaximalLength':            DATA_CONSTRAINT_LENGTH_MAXIMAL,
            'Set':                      DATA_CONSTRAINT_SET,
            'Pattern':                  DATA_CONSTRAINT_PATTERN,
            'MaximalExclusive':         DATA_CONSTRAINT_VALUE_MAXIMAL_EXCLUSIVE,
            'MaximalInclusive':         DATA_CONSTRAINT_VALUE_MAXIMAL_INCLUSIVE,
            'MinimalExclusive':         DATA_CONSTRAINT_VALUE_MINIMAL_EXCLUSIVE,
            'MinimalInclusive':         DATA_CONSTRAINT_VALUE_MINIMAL_INCLUSIVE,
            'Unit':                     DATA_CONSTRAINT_UNIT,
            'ContentType':              DATA_CONSTRAINT_CONTENT_TYPE,
            'FullyQualifiedIdentifier': DATA_CONSTRAINT_IDENTIFIER,
            'Schema':                   DATA_CONSTRAINT_SCHEMA
        }
        self.constraints_basic_allowed_types = {
            'Length':                   ['String', 'Binary'],
            'MinimalLength':            ['String', 'Binary'],
            'MaximalLength':            ['String', 'Binary'],
            'Set':                      ['String', 'Integer', 'Real', 'Date', 'Time', 'Timestamp'],
            'Pattern':                  ['String'],
            'MaximalExclusive':         ['Integer', 'Real', 'Date', 'Time', 'Timestamp'],
            'MaximalInclusive':         ['Integer', 'Real', 'Date', 'Time', 'Timestamp'],
            'MinimalExclusive':         ['Integer', 'Real', 'Date', 'Time', 'Timestamp'],
            'MinimalInclusive':         ['Integer', 'Real', 'Date', 'Time', 'Timestamp'],
            'Unit':                     ['Integer', 'Real'],
            'ContentType':              ['String', 'Binary'],
            'FullyQualifiedIdentifier': ['String'],
            'Schema':                   ['String', 'Binary']
        }
        self.constraints_list = {
            'ElementCount':             DATA_CONSTRAINT_ELEMENTS_COUNT,
            'MinimalElementCount':      DATA_CONSTRAINT_ELEMENTS_MINIMAL,
            'MaximalElementCount':      DATA_CONSTRAINT_ELEMENTS_MAXIMAL
        }
        self.sila_data_types = ['String', 'Binary', 'Integer', 'Real', 'Date', 'Time', 'Timestamp']

    def test_basic(self):
        from ._data_type_constrained import DATA_BASIC

        obj = ConstrainedType(objectify.fromstring(DATA_BASIC).Constrained)
        self.assertIs(type(obj.sub_type), BasicType)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_constrained)

    def test_list(self):
        from ._data_type_constrained import DATA_LIST

        obj = ConstrainedType(objectify.fromstring(DATA_LIST).Constrained)
        self.assertIs(type(obj.sub_type), ListType)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_constrained)

    def test_invalid_subtype_constrained(self):
        from ._data_type_constrained import DATA_CONSTRAINED

        with self.assertRaises(SubDataTypeError):
            _ = ConstrainedType(objectify.fromstring(DATA_CONSTRAINED).Constrained)

    def test_invalid_subtype_structure(self):
        from ._data_type_constrained import DATA_STRUCTURE

        with self.assertRaises(SubDataTypeError):
            _ = ConstrainedType(objectify.fromstring(DATA_STRUCTURE).Constrained)

    @unittest.skip("Undefined behaviour, constraints have no identifier.")
    def test_data_type_identifier(self):
        from ._data_type_constrained import DATA_DATA_TYPE_IDENTIFIER

        obj = ConstrainedType(objectify.fromstring(DATA_DATA_TYPE_IDENTIFIER).Constrained)
        self.assertIs(type(obj.sub_type), DataTypeIdentifier)
        self.assertEqual(obj.name, '')
        self.assertEqual(obj.description, '')
        self.assertEqual(obj.identifier, '')
        self.assertTrue(obj.is_constrained)

    def test_basic_constraints(self):
        # for this test we want to ignore all warnings
        import warnings
        warnings.simplefilter("ignore")

        from ._data_type_constrained import DATA_BASIC_TEMPLATE

        for constraint in self.constraints_basic:
            for basic_data_type in self.constraints_basic_allowed_types[constraint]:
                input_xml = DATA_BASIC_TEMPLATE.format(
                    constraint=self.constraints_basic[constraint],
                    basic_data_type=basic_data_type
                )
                obj = ConstrainedType(objectify.fromstring(input_xml).Constrained)

                with self.subTest(constraint=constraint):
                    self.assertIsNotNone(obj[constraint])

    def test_list_constraints(self):
        # for this test we want to ignore all warnings
        import warnings
        warnings.simplefilter("ignore")

        from ._data_type_constrained import DATA_LIST_TEMPLATE

        for constraint in self.constraints_list:
            input_xml = DATA_LIST_TEMPLATE.format(constraint=self.constraints_list[constraint])
            obj = ConstrainedType(objectify.fromstring(input_xml).Constrained)

            with self.subTest(constraint=constraint):
                self.assertIsNotNone(obj[constraint])

    def test_constraint_length(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_LENGTH_TEMPLATE

        def _create_object(_basic_type, _length) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_LENGTH_TEMPLATE.format(
                    length=str(_length)
                ),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            # test valid length(s)
            current_lengths = [42]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['Length']:
                        # allowed
                        obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertEqual(obj.constraint_length, current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertIsNone(obj.constraint_length)
            # test invalid length(s)
            current_lengths = [-42, 0, 1.3]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['Length']:
                        # allowed
                        with self.assertWarns(ConstraintValueWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    self.assertIsNone(obj.constraint_length)

    def test_constraint_minimal_length(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_LENGTH_MINIMAL_TEMPLATE

        def _create_object(_basic_type, _length) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_LENGTH_MINIMAL_TEMPLATE.format(
                    length=str(_length)
                ),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            # test valid length(s)
            current_lengths = [42]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['MinimalLength']:
                        # allowed
                        obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertEqual(obj.constraint_length_minimal, current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertIsNone(obj.constraint_length_minimal)
            # test invalid length(s)
            current_lengths = [-42, 0, 1.3]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['MinimalLength']:
                        # allowed
                        with self.assertWarns(ConstraintValueWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    self.assertIsNone(obj.constraint_length_minimal)

    def test_constraint_maximal_length(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_LENGTH_MAXIMAL_TEMPLATE

        def _create_object(_basic_type, _length) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_LENGTH_MAXIMAL_TEMPLATE.format(
                    length=str(_length)
                ),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            # test valid length(s)
            current_lengths = [42]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['MaximalLength']:
                        # allowed
                        obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertEqual(obj.constraint_length_maximal, current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                        self.assertIsNone(obj.constraint_length_maximal)
            # test invalid length(s)
            current_lengths = [-42, 0, 1.3]
            for current_length in current_lengths:
                with self.subTest(basic_type=basic_type, length=current_length):
                    if basic_type in self.constraints_basic_allowed_types['MaximalLength']:
                        # allowed
                        with self.assertWarns(ConstraintValueWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    else:
                        # not allowed, should find nothing
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _length=current_length)
                    self.assertIsNone(obj.constraint_length_maximal)

    def test_constraint_element_count(self):
        # for this test we want to ignore all warnings
        import warnings
        warnings.simplefilter("ignore")

        from ._data_type_constrained import DATA_LIST_TEMPLATE, DATA_CONSTRAINT_ELEMENTS_COUNT_TEMPLATE

        def _create_object(_count) -> ConstrainedType:
            input_xml = DATA_LIST_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_ELEMENTS_COUNT_TEMPLATE.format(
                    number=str(_count)
                ),
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        # test valid count(s)
        current_counts = [42]
        for current_count in current_counts:
            with self.subTest(count=current_count):
                obj = _create_object(_count=current_count)
                self.assertEqual(obj.constraint_elements_count, current_count)
        # test invalid count(s)
        current_counts = [-42, 0, 1.3]
        for current_count in current_counts:
            with self.subTest(_count=current_count):
                with self.assertWarns(ConstraintValueWarning):
                    obj = _create_object(_count=current_count)
                self.assertIsNone(obj.constraint_elements_count)

    def test_constraint_minimal_element_count(self):
        # for this test we want to ignore all warnings
        import warnings
        warnings.simplefilter("ignore")

        from ._data_type_constrained import DATA_LIST_TEMPLATE, DATA_CONSTRAINT_ELEMENTS_MINIMAL_TEMPLATE

        def _create_object(_count) -> ConstrainedType:
            input_xml = DATA_LIST_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_ELEMENTS_MINIMAL_TEMPLATE.format(
                    number=str(_count)
                ),
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        # test valid count(s)
        current_counts = [42]
        for current_count in current_counts:
            with self.subTest(count=current_count):
                obj = _create_object(_count=current_count)
                self.assertEqual(obj.constraint_elements_minimal, current_count)
        # test invalid count(s)
        current_counts = [-42, 0, 1.3]
        for current_count in current_counts:
            with self.subTest(_count=current_count):
                with self.assertWarns(ConstraintValueWarning):
                    obj = _create_object(_count=current_count)
                self.assertIsNone(obj.constraint_elements_minimal)

    def test_constraint_maximal_element_count(self):
        # for this test we want to ignore all warnings
        import warnings
        warnings.simplefilter("ignore")

        from ._data_type_constrained import DATA_LIST_TEMPLATE, DATA_CONSTRAINT_ELEMENTS_MAXIMAL_TEMPLATE

        def _create_object(_count) -> ConstrainedType:
            input_xml = DATA_LIST_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_ELEMENTS_MAXIMAL_TEMPLATE.format(
                    number=str(_count)
                ),
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        # test valid count(s)
        current_counts = [42]
        for current_count in current_counts:
            with self.subTest(count=current_count):
                obj = _create_object(_count=current_count)
                self.assertEqual(obj.constraint_elements_maximal, current_count)
        # test invalid count(s)
        current_counts = [-42, 0, 1.3]
        for current_count in current_counts:
            with self.subTest(_count=current_count):
                with self.assertWarns(ConstraintValueWarning):
                    obj = _create_object(_count=current_count)
                self.assertIsNone(obj.constraint_elements_maximal)

    def test_constraint_set(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_SET

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_SET,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['Set']:
                    # allowed
                    obj = _create_object(_basic_type=basic_type)
                    self.assertCountEqual(['A', 'B', 'C'], obj.constraint_set)
                else:
                    # not allowed
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_set)

    def test_constraint_pattern(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_PATTERN

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_PATTERN,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['Pattern']:
                    # allowed
                    obj = _create_object(_basic_type=basic_type)
                    self.assertEqual('[a-zA-Z0-9_]', obj.constraint_pattern)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_pattern)

    def test_constraint_max_exclusive(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_VALUE_MAXIMAL_EXCLUSIVE

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_VALUE_MAXIMAL_EXCLUSIVE,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['MaximalExclusive']:
                    obj = _create_object(_basic_type=basic_type)
                    self.assertEqual('42', obj.constraint_value_maximal_exclusive)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_value_maximal_exclusive)

    def test_constraint_min_exclusive(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_VALUE_MINIMAL_EXCLUSIVE

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_VALUE_MINIMAL_EXCLUSIVE,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['MinimalExclusive']:
                    obj = _create_object(_basic_type=basic_type)
                    self.assertEqual('42', obj.constraint_value_minimal_exclusive)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_value_minimal_exclusive)

    def test_constraint_max_inclusive(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_VALUE_MAXIMAL_INCLUSIVE

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_VALUE_MAXIMAL_INCLUSIVE,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['MaximalInclusive']:
                    obj = _create_object(_basic_type=basic_type)
                    self.assertEqual('42', obj.constraint_value_maximal_inclusive)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_value_maximal_inclusive)

    def test_constraint_min_inclusive(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_VALUE_MINIMAL_INCLUSIVE

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_VALUE_MINIMAL_INCLUSIVE,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['MinimalInclusive']:
                    obj = _create_object(_basic_type=basic_type)
                    self.assertEqual('42', obj.constraint_value_minimal_inclusive)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_value_minimal_inclusive)

    def test_constraint_unit(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_UNIT

        def _create_object(_basic_type) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_UNIT,
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['Unit']:
                    obj = _create_object(_basic_type=basic_type)

                    self.assertEqual(obj.constraint_unit.label, 'Unit-Label')
                    self.assertEqual(obj.constraint_unit.unit_components[0].exponent, 1)
                    self.assertEqual(obj.constraint_unit.unit_components[0].factor, 1)
                    self.assertEqual(obj.constraint_unit.unit_components[0].offset, 0)
                    self.assertEqual(obj.constraint_unit.unit_components[0].si_unit.value, '-')
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_unit)

    def test_constraint_content_type(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_CONTENT_TYPE, \
            DATA_CONSTRAINT_CONTENT_TYPE_UNSUPPORTED

        def _create_object(_basic_type, supported: bool = True) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=(DATA_CONSTRAINT_CONTENT_TYPE if supported else DATA_CONSTRAINT_CONTENT_TYPE_UNSUPPORTED),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['ContentType']:
                    with self.subTest(supported=True):
                        obj = _create_object(_basic_type=basic_type, supported=True)
                        self.assertEqual(obj.constraint_content_type.type, 'application')
                        self.assertEqual(obj.constraint_content_type.subtype, 'xml')
                        self.assertEqual(
                            obj.constraint_content_type.parameters,
                            {
                                'charset': 'utf-8',
                                'parameter': 'value'
                            }
                        )
                    with self.subTest(supported=False):
                        with self.assertWarns(ConstraintUnsupportedContentType):
                            obj = _create_object(_basic_type=basic_type, supported=False)
                        self.assertEqual(obj.constraint_content_type.type, 'type')
                        self.assertEqual(obj.constraint_content_type.subtype, 'subtype')
                        self.assertFalse(obj.constraint_content_type.parameters)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type)
                    self.assertIsNone(obj.constraint_content_type)

    def test_constraint_fully_qualified_identifier(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_IDENTIFIER_TEMPLATE

        def _create_object(_basic_type, _identifier) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_IDENTIFIER_TEMPLATE.format(
                    identifier=_identifier
                ),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            current_identifiers = ['FeatureIdentifier', 'CommandIdentifier', 'CommandParameterIdentifier',
                                   'CommandResponseIdentifier', 'IntermediateCommandResponseIdentifier',
                                   'DefinedExecutionErrorIdentifier', 'PropertyIdentifier', 'DataTypeIdentifier',
                                   'MetaDataIdentifier']
            for current_identifier in current_identifiers:
                with self.subTest(basic_type=basic_type):
                    if basic_type in self.constraints_basic_allowed_types['FullyQualifiedIdentifier']:
                        obj = _create_object(_basic_type=basic_type, _identifier=current_identifier)
                        self.assertEqual(obj.constraint_identifier, current_identifier)
                    else:
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _identifier=current_identifier)
                        self.assertIsNone(obj.constraint_identifier)
            current_identifiers = ['a', 'b', 'c']
            for current_identifier in current_identifiers:
                with self.subTest(basic_type=basic_type):
                    if basic_type in self.constraints_basic_allowed_types['FullyQualifiedIdentifier']:
                        with self.assertWarns(ConstraintValueWarning):
                            obj = _create_object(_basic_type=basic_type, _identifier=current_identifier)
                    else:
                        with self.assertWarns(ConstraintTypeWarning):
                            obj = _create_object(_basic_type=basic_type, _identifier=current_identifier)
                    self.assertIsNone(obj.constraint_identifier)

    def test_constraint_schema(self):

        from ._data_type_constrained import DATA_BASIC_TEMPLATE, DATA_CONSTRAINT_SCHEMA_TEMPLATE

        def _create_object(_basic_type, _type, _data) -> ConstrainedType:
            input_xml = DATA_BASIC_TEMPLATE.format(
                constraint=DATA_CONSTRAINT_SCHEMA_TEMPLATE.format(
                    type=_type,
                    data=_data
                ),
                basic_data_type=_basic_type
            )
            return ConstrainedType(objectify.fromstring(input_xml).Constrained)

        for basic_type in self.sila_data_types:
            with self.subTest(basic_type=basic_type):
                if basic_type in self.constraints_basic_allowed_types['Schema']:
                    # Xml / Url
                    obj = _create_object(_basic_type=basic_type,
                                         _type='Xml',
                                         _data='<Url>http://www.w3.org/2001/XMLSchema</Url>')
                    self.assertEqual(obj.constraint_schema.type.value, 'Xml')
                    self.assertEqual(obj.constraint_schema.url, 'http://www.w3.org/2001/XMLSchema')
                    self.assertIsNone(obj.constraint_schema.inline)
                    # Xml / Inline
                    obj = _create_object(_basic_type=basic_type,
                                         _type='Xml',
                                         _data='<Inline>test</Inline>')
                    self.assertEqual(obj.constraint_schema.type.value, 'Xml')
                    self.assertEqual(obj.constraint_schema.inline, 'test')
                    self.assertIsNone(obj.constraint_schema.url)
                    # Json / Url
                    obj = _create_object(_basic_type=basic_type,
                                         _type='Json',
                                         _data='<Url>http://www.w3.org/2001/XMLSchema</Url>')
                    self.assertEqual(obj.constraint_schema.type.value, 'Json')
                    self.assertEqual(obj.constraint_schema.url, 'http://www.w3.org/2001/XMLSchema')
                    self.assertIsNone(obj.constraint_schema.inline)
                    # Json / Inline
                    obj = _create_object(_basic_type=basic_type,
                                         _type='Json',
                                         _data='<Inline>test</Inline>')
                    self.assertEqual(obj.constraint_schema.type.value, 'Json')
                    self.assertEqual(obj.constraint_schema.inline, 'test')
                    self.assertIsNone(obj.constraint_schema.url)
                else:
                    with self.assertWarns(ConstraintTypeWarning):
                        obj = _create_object(_basic_type=basic_type,
                                             _type='Xml',
                                             _data='<Url>http://www.w3.org/2001/XMLSchema</Url>')
                    self.assertIsNone(obj.constraint_schema)
        # let us test some completely invalid schema constraints
        with self.subTest(basic_type='String', type='Invalid', data='<Url>http://www.w3.org/2001/XMLSchema</Url>'):
            with self.assertWarns(ConstraintValueWarning):
                obj = _create_object(_basic_type='String',
                                     _type='Invalid',
                                     _data='<Url>http://www.w3.org/2001/XMLSchema</Url>')
            self.assertIsNone(obj.constraint_schema)
        with self.subTest(basic_type='String', type='Xml', data='<NoData>Fooled Ya!</NoData>'):
            with self.assertWarns(ConstraintValueWarning):
                obj = _create_object(_basic_type='String',
                                     _type='Invalid',
                                     _data='<NoData>Fooled Ya!</NoData>')
            self.assertIsNone(obj.constraint_schema)

    # TODO: Check constraints
    #  * Multiple constraints at once
    #  * Setting constraints via dictionary access
