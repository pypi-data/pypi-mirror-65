"""
Common configuration variables which are consistent across the system
"""
import os
import configparser
import pathlib
import logging
from typing import Union

logger = logging.getLogger(__name__)
logger.debug('defining aghplctools configuration variables')
_config_ini_location = 'C:\\ProgramData\\Agilent Technologies\\ChemStation\\ChemStation.ini'
_config = configparser.ConfigParser()
_result = _config.read(
    _config_ini_location,
    encoding='utf16',
)
if _result:
    logger.debug('ChemStation configuration INI located, values will be read from this')
else:
    logger.debug('no configuration INI found, attempting to load from environment variables and defaults')


def _retrieve_value(ini_path: tuple,
                    env_name: str,
                    default: Union[str, None],
                    ) -> Union[str, None]:
    """
    Attempts to retrieve a variable value from
        1) the ChemStation configuration INI
        2) an environment variable
    If no value is found for either, the variable default value is returned

    :param ini_path: ini path to find the value
    :param env_name: environment variable name
    :param default: default value
    :return:
    """
    # todo support multiple enviornment variable names
    if _result:  # if ini loading was successful
        return _config.get(*ini_path)
    else:
        return os.getenv(
            env_name,
            default,
        )


# installation path for ChemStation
CHEMSTATION_INSTALL_PATH: pathlib.Path = pathlib.Path(
    _retrieve_value(
        ('PCS', 'Path'),
        '',  # todo
        '',
    )
)
logger.debug(f'installation path: {CHEMSTATION_INSTALL_PATH}')

# core installation path for ChemStation
CHEMSTATION_CORE_PATH: pathlib.Path = pathlib.Path(
    _retrieve_value(
        ('PCS,1', '_EXEPATH$'),
        '',  # todo
        '',
    )
)
logger.debug(f'core path: {CHEMSTATION_CORE_PATH}')

# path for HPLC data storage
CHEMSTATION_DATA_PATH: pathlib.Path = pathlib.Path(
    _retrieve_value(
        ('PCS,1', '_DATAPATH$'),
        'hplcfolder',
        'C:\\Chem32',
    )
)
logger.debug(f'data path: {CHEMSTATION_DATA_PATH}')
if os.path.isdir(CHEMSTATION_DATA_PATH) is False:
    logger.warning(
        'The hplcfolder envrionment variable is not set on this computer '
        'and the default folder does not exist, functionality will be reduced.'
    )

# method storage path
CHEMSTATION_METHOD_PATH: pathlib.Path = pathlib.Path(
    _retrieve_value(
        ('PCS,1', '_CONFIGMETPATH$'),
        '',  # todo
        '',
    )
)
logger.debug(f'method path: {CHEMSTATION_METHOD_PATH}')

# chemstation version
CHEMSTATION_VERSION: str = _retrieve_value(
    ('PCS', 'REV'),
    '',  # todo
    '0'
)
logger.debug(f'ChemStation version: {CHEMSTATION_VERSION}')
