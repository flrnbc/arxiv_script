"""
Helper function to check if path exists
as directory or file. Another helper function
for opening a downloaded file.
"""

import platform
import os


def check_path(path, path_type):
    if path_type == "directory":
        return os.path.isdir(path)
    elif path_type == "file":
        return os.path.isfile(path)


def get_opener():
    """
    To view a pdf-file, we use subprocess.call(opener, file_path).
    This calls 'opener file_path' as in a terminal and is hence dependent
    on the operating system:
      - OS X: 'opener = open'
      - Win: 'opener = start'
      - Linux based: 'xdg-open'
    """
    osname = platform.system().lower()
    if 'windows' in osname:
        opener = 'start'
    elif 'osx' in osname or 'darwin' in osname:
        opener = 'open'
    else:
        opener = 'xdg-open'
    return f'{opener}'
