""" Helper function to check if path exists
    as directory or file. Another helper function
    for opening a downloaded file.
"""

import os
import json
import platform

def check_path(path, path_type):
    ''' Check if path is of the given path_type (dir or file). '''
    if path_type == "directory":
        return os.path.isdir(path)
    elif path_type == "file":
        return os.path.isfile(path)

def get_opener():
    """ To view a pdf-file, we use subprocess.call(opener, file_path).
        This calls 'opener file_path' as in a terminal and is hence dependent
        on the operating system:
        - OS X: 'opener = open'
        - Win: 'opener = start'
        - Linux based: 'xdg-open'
    """
    OSNAME = platform.system().lower()
    if 'windows' in OSNAME:
        opener = 'start'
    elif 'osx' in OSNAME or 'darwin' in OSNAME:
        opener = 'open'
    else:
        opener = 'xdg-open'
    return f'{opener}'


# short test
# print(check_saved_path(file = "data", key = "default directory", path_type = "dir"))
# change_path(file = "data", key = "default directory", new_path = "/Users/fbeck/Documents/Math/")
