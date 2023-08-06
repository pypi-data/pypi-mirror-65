"""
Methods and classes borrowed from ada_core. These will eventually be moved to a separate project.
"""

import os
import warnings
import time
import numpy as np


def find_nearest(lst, value, wiggle=None):
    """
    Finds the nearest value in a dictionary or list

    :param lst: sorted list or dictionary with keys that are values
    :param value: value to find
    :param wiggle: the wiggle room that the value needs to be within (the bounds are [value-wiggle, value+wiggle])
    :return: the nearest key in the dictionary to the value
    """
    if len(lst) == 0:  # if there are no values
        return None
    if type(lst) == dict:  # if handed a dictionary
        lst = sorted(lst.keys())
    val = lst[
        np.abs(  # array of absolute differences of each list value to the target
            [val - value for val in lst]
        ).argmin()  # index of the minimum value
    ]
    if wiggle is not None and abs(value - val) > wiggle:  # if it's outside the wiggle area
        return None
    return val


class Watcher(object):
    def __init__(self,
                 path,
                 watchfor='',
                 includesubfolders=True,
                 subdirectory=None,
                 ):
        """
        Watches a folder for file changes.

        :param path: The folder path to watch for changes
        :param watchfor: Watch for this item. This can be a full filename, or an extension (denoted by *., e.g. "*.ext")
        :param bool includesubfolders: wehther to search subfolders
        :param str subdirectory: specified subdirectory
        """
        self._path = None
        self._subdir = None
        self.path = path
        self.subdirectory = subdirectory
        self.includesubfolders = includesubfolders
        self.watchfor = watchfor

    def __repr__(self):
        return f'{self.__class__.__name__}({len(self.contents)} {self.watchfor})'

    def __str__(self):
        return f'{self.__class__.__name__} with {len(self.contents)} matches of {self.watchfor}'

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        for file in self.contents:
            yield file

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, newpath):
        if not os.path.isdir(newpath):
            raise ValueError(f'The specified path\n{newpath}\ndoes not exist.')
        self._path = newpath

    @property
    def subdirectory(self):
        return self._subdir

    @subdirectory.setter
    def subdirectory(self, newdir):
        if newdir is None:
            del self.subdirectory
            return
        if not os.path.isdir(
            os.path.join(self.path, newdir)
        ):
            raise ValueError(f'The subdirectory {newdir} does not exist in the path {self.path}.')
        self._subdir = newdir

    @subdirectory.deleter
    def subdirectory(self):
        self._subdir = None

    @property
    def contents(self):
        """Finds all instances of the watchfor item in the path"""
        # TODO exclude subfolders if specified
        if self.subdirectory is not None:
            path = os.path.join(self.path, self.subdirectory)
        else:
            path = self._path
        contents = []
        if self.includesubfolders is True:
            for root, dirs, files in os.walk(path):  # walk through specified path
                for filename in files:  # check each file
                    if filename.lower().endswith(self.watchfor[1:].lower()):  # if extension matches
                        contents.append(os.path.join(root, filename))
                    elif filename.lower() == self.watchfor.lower():  # if filename match
                        contents.append(os.path.join(root, filename))
        else:
            for file in os.listdir(path):
                if file.lower().endswith(self.watchfor[1:].lower()):
                    contents.append(os.path.join(path, file))
                elif file.lower() == self.watchfor.lower():
                    contents.append(os.path.join(path, file))
        return contents

    def check_path_for_files(self):
        """Finds all instances of the watchfor item in the path"""
        warnings.warn('The check_path_for_files method has be depreciated, access .contents directly',
                      DeprecationWarning)
        return self.contents

    def find_subfolder(self):
        """returns the subdirectory path within the full path where the target file is"""
        if self.subdirectory is not None:
            path = os.path.join(self.path, self.subdirectory)
        else:
            path = self.path
        contents = []
        for root, dirs, files in os.walk(path):  # walk through specified path
            for filename in files:  # check each file
                if filename.lower().endswith(self.watchfor[1:].lower()):  # if extension matches
                    contents.append(root)
                elif filename.lower() == self.watchfor.lower():  # if filename match
                    contents.append(root)
        return contents

    def wait_for_presence(self, waittime=1.):
        """waits for a specified match to appear in the watched path"""
        while len(self.contents) == 0:
            time.sleep(waittime)
        return True

    def oldest_instance(self, wait=False, **kwargs):
        """
        Retrieves the first instance of the watched files.

        :param wait: if there are no instances, whether to wait for one to appear
        :return: path to first instance (None if there are no files present)
        """
        if len(self.contents) == 0:  # if there are no files
            if wait is True:  # if waiting is specified
                self.wait_for_presence(**kwargs)
            else:  # if no wait and no files present, return None
                return None
        if len(self.contents) == 1:  # if there is only one file
            return os.path.join(self._path, self.contents[0])
        else:  # if multiple items in list
            return os.path.join(  # return path to oldest (last modified) file in directory
                self._path,
                min(
                    zip(
                        self.contents,  # files in directory
                        [os.path.getmtime(  # last modifiation time for files in directory
                                               os.path.join(self._path, filename)
                                               ) for filename in self.contents]
                    ),
                    key=lambda x: x[1]
                )[0]
            )

    def newest_instance(self):
        """
        Retrieves the newest instance of the watched files.

        :return: path to newest instance
        :rtype: str
        """
        if len(self.contents) == 0:  # if there are no files
            # if wait is True:  # if waiting is specified
            #     self.wait_for_presence(**kwargs)
            # else:  # if no wait and no files present, return None
                return None
        if len(self.contents) == 1:  # if there is only one file
            return os.path.join(self._path, self.contents[0])
        else:  # if multiple items in list
            return os.path.join(  # return path to oldest (last modified) file in directory
                self._path,
                max(
                    zip(
                        self.contents,  # files in directory
                        [os.path.getmtime(  # last modifiation time for files in directory
                            os.path.join(self._path, filename)
                        ) for filename in self.contents]
                    ),
                    key=lambda x: x[1]
                )[0]
            )

    def update_path(self, newpath):
        """
        Updates the path to file of the instance.

        :param str newpath: path to new file
        """
        warnings.warn('The update_path method has been depreciated, modify .path directly', DeprecationWarning)
        self.path = newpath


def front_pad(lst, length, pad=0.):
    """
    Front pads a list to the specified length with the provided value.

    :param lst: list to pad
    :param length: target length
    :return: padded list
    """
    return [pad] * (length - len(lst)) + lst
