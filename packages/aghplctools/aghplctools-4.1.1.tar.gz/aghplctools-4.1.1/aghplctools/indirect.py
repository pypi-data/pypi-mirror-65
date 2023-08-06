"""tools for indirect run control of ChemStation"""
import os
import re
import pathlib
from typing import Union, Tuple
from hein_utilities.files import Watcher
from .config import CHEMSTATION_DATA_PATH


# storage for acquiring path 
_acquiring_path: pathlib.Path = None

# acqiring parser
_acq_re = re.compile(
    'CURRDATAFILE:(?P<file_number>\d+)\|(?P<file_name>[^\n]+)'
)


def locate_acquiring_file(search_path: Union[str, pathlib.Path] = None) -> pathlib.Path:
    """
    determines the path for ACQUIRING.TXT

    :param search_path: search path. If not specified, uses CHEMSTATION_DATA_PATH
    :return: file path for ACQUIRING.TXT
    """
    global _acquiring_path
    if search_path is None:
        search_path = CHEMSTATION_DATA_PATH
    watch = Watcher(
        path=search_path,
        watchfor='ACQUIRING\.TXT',
    )
    contents = watch.contents
    if len(contents) == 0:
        raise ValueError(f'ACQUIRING.TXT was not found in {search_path}, are you sure a sequence is running?')
    elif len(contents) > 1:
        tab = '\t'
        discovered = f'{f"{tab}".join(contents)}'
        raise ValueError(
            'More than one instance of ACQUIRING.TXT was found. Please remove the extra file. \n'
            f'discovered paths: {discovered}'
        )
    _acquiring_path = contents[0]
    return contents[0]


def _check_current():
    """finds an acquiring file if undefined and checks whether the file exists"""
    global _acquiring_path
    if _acquiring_path is None or os.path.isfile(_acquiring_path) is False:
        locate_acquiring_file()


def sequence_is_running() -> bool:
    """returns whether a sequence is running"""
    try:
        # checks for a file
        _check_current()
        return True
    except ValueError:
        # if an error is raised, something is wrong
        return False


def current_num_and_file() -> Tuple[int, str]:
    """
    Returns the current number in the sequence and the name of the data file being acquired.

    :return: current file number, current file name
    """
    _check_current()
    with open(_acquiring_path, 'rt', encoding='utf16') as f:
        contents = f.read()
    match = _acq_re.search(contents)
    if match is None:
        raise ValueError('The contents of ACQUIRING.TXT could not be parsed.')
    return (
        int(match.group('file_number')),
        match.group('file_name')
    )


def current_file() -> str:
    """
    Returns the current data file name being acquired (next up in the sequence)

    :return: data file name
    """
    return current_num_and_file()[1]


def current_file_path() -> pathlib.Path:
    """
    Returns the full path for the file name being acquired (next up in the sequence)

    :return: full path to the data file
    """
    _check_current()
    current_path = pathlib.Path(_acquiring_path)
    return current_path.parent / current_file()
