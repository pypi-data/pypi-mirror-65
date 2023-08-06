
import logging
import os
import uuid
from configparser import ConfigParser


def get_config_dir(subdir: str = None) -> str:
    if os.environ.get('APPDATA'):
        path = os.path.join(os.environ.get('APPDATA'), 'SiLA2')
    else:
        path = os.path.join(os.environ['HOME'], '.config', 'sila2')

    if subdir is not None:
        return os.path.join(path, subdir)


def read_config_file(section: str, name: str) -> ConfigParser:
    """
    Reads and (re-)writes the config file and/or fills it with default values.
    """
    config_dir = get_config_dir(subdir=name)

    sila2_config_file = os.path.join(config_dir, name + '.conf')
    logging.debug("Reading config from {config_file}".format(config_file=sila2_config_file))

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logging.info("Creating config directory {config_dir}.".format(config_dir=config_dir))

    sila2_config = ConfigParser()
    try:
        sila2_config.read(sila2_config_file)
    except Exception as err:
        logging.error(
            (
                'Failed reading config file: {err}' '\n'
                'Using default values.'
            ).format(err=err))

    # populate the config with values
    #   define the config sections
    if 'server' not in sila2_config:
        sila2_config['server'] = {}
    #   SERVER section
    #       UUID
    if 'UUID' not in sila2_config['server']:
        _config_uuid = str(uuid.uuid4())
        logging.debug("UUID: {uuid}".format(uuid=_config_uuid))
        sila2_config['server']['UUID'] = _config_uuid

    # (re-)write the config file
    with open(sila2_config_file, 'w') as file_config:
        sila2_config.write(file_config)

    return sila2_config