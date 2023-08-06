"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Framework utilities*

:details: helper functions for framework files that can provide files from the standard feature library

:file:    utilities.py
:authors: Mark Doerr
          Timm Severin

:date: (creation)          2019-08-20
:date: (last modification) 2019-08-28
________________________________________________________________________
"""

import logging

from typing import Optional

import os
from shutil import copy2


def copy_framework_xml(target_dir: str, feature: str) -> bool:
    """
    Copies the XML/FDL file of a standard feature to the target directory.

    :param target_dir: The directory to where the files should be copied.
    :param feature: The name of the feature to copy.

    :return: Whether the copy operation was successful or not.
    """

    xml_input_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'feature_definitions'
    )
    file_name = '{feature}.sila.xml'.format(feature=feature)
    file_path = _find_file(base_dir=xml_input_dir, name=file_name)

    if file_path is None:
        return False

    return _copy_file(file=file_path, target_dir=target_dir)


def copy_framework_service(target_dir: str, feature: str) -> bool:
    """
    This function can be used to obtain service files for framework standard features.
        It copies the service files for the requested feature (`_pb2.py` and `_pb2_grpc.py`) to the target directory.

    :param target_dir: The directory to where the files should be copied.
    :param feature: The name of the feature to copy.

    :return: Whether the copy operation was successful or not.

    .. note:: The standard feature "SilaService" and "SimulationController" are strongly tied to the base implementation
              of the SilAServer class, and thus are not available to copy via this function.
    """

    if feature in ['SiLAService', 'SimulationController']:
        logging.error(
            '{feature} is strongly coupled to the base SiLAServer and is not meant to be modified. '
            'Copying it out of the library is thus not possible via this function.'.format(
                feature=feature
            )
        )
        return False

    service_input_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'std_features'
    )

    file_name_pb2 = '{feature}_pb2.py'.format(feature=feature)
    file_path_pb2 = _find_file(base_dir=service_input_dir, name=file_name_pb2)

    file_name_pb2_grpc = '{feature}_pb2_grpc.py'.format(feature=feature)
    file_path_pb2_grpc = _find_file(base_dir=service_input_dir, name=file_name_pb2_grpc)

    if file_path_pb2 is None or file_path_pb2_grpc is None:
        return False

    return (
        _copy_file(file=file_path_pb2, target_dir=target_dir) &
        _copy_file(file=file_path_pb2_grpc, target_dir=target_dir)
    )


def copy_framework_proto(target_dir: str, feature: str) -> bool:
    """
    This function can be used to obtain the proto files for framework standard features.
        It copies the protobuffer definitions for the requested feature (`_pb2.py` and `_pb2_grpc.py`) to the target
        directory.

    :param target_dir: The directory to where the files should be copied.
    :param feature: The name of the feature to copy.

    :return:  Whether the copy operation was successful or not.
    """

    proto_input_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'protobuf'
    )
    file_name = '{feature}.proto'.format(feature=feature)
    file_path = _find_file(base_dir=proto_input_dir, name=file_name)

    if file_path is None:
        return False

    return _copy_file(file=file_path, target_dir=target_dir)


def copy_silastandard_proto(target_dir: str) -> bool:
    """
    Convenience function to copy the proto files from the SiLA standard to a target directory.

    :param target_dir: The directory to which the files should be copied.

    :return: Success of the copy operation.
    """
    return (
        copy_framework_proto(target_dir=target_dir, feature='SiLAFramework') &
        copy_framework_proto(target_dir=target_dir, feature='SiLABinaryTransfer')
    )


def _copy_file(file: str, target_dir: str) -> bool:
    try:
        copy2(file, target_dir)
    except Exception as err:
        logging.exception('Cannot copy file {filename} to target directory "{target}": {err}'.format(
            filename=file,
            target=target_dir,
            err=err
        ))
        return False

    return True

def _find_file(base_dir: str, name: str) -> Optional[str]:
    """
    Find a file path in a directory and it's subdirectories, return the first match

    :param base_dir: The base directory in which to search for the file.
    :param name: The name of the file for which to search.

    :return: The path (including `base_dir`) or None if the file was not found.
    """

    # recursively walk through all directories, start at the base_dir until the file is found
    for (root, dirs, files) in os.walk(base_dir, topdown=True):
        if name in files:
            return os.path.join(root, name)

    return None
