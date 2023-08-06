import unittest

import logging

import tempfile
import shutil
import os
import filecmp

from ..utilities import copy_framework_xml, copy_framework_service, copy_framework_proto
from ..utilities import copy_silastandard_proto
from ..utilities import _find_file


class TestUtilities(unittest.TestCase):

    def setUp(self):
        # generate the directory with which we work
        self.target_dir = tempfile.mkdtemp(suffix='_test', prefix='sila2lib.framework_')

        # defined standard features in the library
        self.feature_ids = [
            'AuthenticationService',
            'AuthorizationService',
            'CancelController',
            'LockController',
            'ObservableCommandController',
            'ParameterConstraintProvider',
        ]

        # features that require special attention
        self.special_feature_ids = [
            'SiLAService',
            'SimulationController'
        ]

        # disable logging
        logging.disable(logging.CRITICAL)

    def tearDown(self) -> None:
        # make sure to remove the temporary directory
        shutil.rmtree(self.target_dir)

    def test_copy_framework_xml(self):
        for feature_id in self.feature_ids + self.special_feature_ids:
            with self.subTest(feature_id=feature_id):
                _expected_filename = '{feature}.sila.xml'.format(feature=feature_id)
                # copy the file
                self.assertTrue(copy_framework_xml(target_dir=self.target_dir, feature=feature_id))
                # make sure it really exists
                self.assertTrue(os.path.exists(os.path.join(self.target_dir, _expected_filename)))
                # make sure the file is the same as the one supplied in this library
                self.assertTrue(filecmp.cmp(
                    f1=_find_file(
                        base_dir=os.path.join(os.path.dirname(__file__), '..', 'feature_definitions'),
                        name=_expected_filename
                    ),
                    f2=os.path.join(self.target_dir, _expected_filename),
                    shallow=False
                ))

    def test_copy_framework_service(self):
        for feature_id in self.feature_ids:
            with self.subTest(feature_id=feature_id):
                _expected_filename_pb2 = '{feature}_pb2.py'.format(feature=feature_id)
                _expected_filename_pb2_grpc = '{feature}_pb2_grpc.py'.format(feature=feature_id)
                # copy the file
                self.assertTrue(copy_framework_service(target_dir=self.target_dir, feature=feature_id))
                # make sure they really exists
                self.assertTrue(os.path.exists(os.path.join(self.target_dir, _expected_filename_pb2)))
                self.assertTrue(os.path.exists(os.path.join(self.target_dir, _expected_filename_pb2_grpc)))
                # make sure the file is the same as the one supplied in this library
                self.assertTrue(filecmp.cmp(
                    f1=_find_file(
                        base_dir=os.path.join(os.path.dirname(__file__), '..', 'std_features'),
                        name=_expected_filename_pb2
                    ),
                    f2=os.path.join(self.target_dir, _expected_filename_pb2),
                    shallow=False
                ))
                self.assertTrue(filecmp.cmp(
                    f1=_find_file(
                        base_dir=os.path.join(os.path.dirname(__file__), '..', 'std_features'),
                        name=_expected_filename_pb2_grpc
                    ),
                    f2=os.path.join(self.target_dir, _expected_filename_pb2_grpc),
                    shallow=False
                ))
        for feature_id in self.special_feature_ids:
            with self.subTest(feature_id=feature_id):
                self.assertFalse(copy_framework_service(target_dir=self.target_dir, feature=feature_id))

    def test_copy_framework_proto(self):
        for feature_id in self.feature_ids + self.special_feature_ids:
            with self.subTest(feature_id=feature_id):
                _expected_filename = '{feature}.proto'.format(feature=feature_id)
                # copy the file
                self.assertTrue(copy_framework_proto(target_dir=self.target_dir, feature=feature_id))
                # make sure it really exists
                self.assertTrue(os.path.exists(os.path.join(self.target_dir, _expected_filename)))
                # make sure the file is the same as the one supplied in this library
                self.assertTrue(filecmp.cmp(
                    f1=_find_file(
                        base_dir=os.path.join(os.path.dirname(__file__), '..', 'protobuf'),
                        name=_expected_filename
                    ),
                    f2=os.path.join(self.target_dir, _expected_filename),
                    shallow=False
                ))

    def test_copy_silastandard_proto(self):
        # copy the files
        self.assertTrue(copy_silastandard_proto(target_dir=self.target_dir))
        for feature_proto in ['SiLAFramework.proto', 'SiLABinaryTransfer.proto']:
            with self.subTest(feature_proto=feature_proto):
                # make sure they exists
                self.assertTrue(os.path.exists(os.path.join(self.target_dir, feature_proto)))
                # compare the contents
                self.assertTrue(filecmp.cmp(
                    f1=os.path.join(os.path.dirname(__file__), '..', 'protobuf', feature_proto),
                    f2=os.path.join(self.target_dir, feature_proto),
                    shallow=False
                ))
