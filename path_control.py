""" Some helper functions to load and change path to
    directory where articles are downloaded to and
    to the bib-file. Another helper function for
    opening a downloaded file.
"""

import os
import json
import platform

def load(file):
    ''' Load a data file as a json object. '''
    with open (file, mode = 'r') as f:
        loaded_data = json.load(f)
    return loaded_data

def check_path(path, path_type):
    ''' Check if path is of the given path_type (dir or file). '''
    if path_type == "dir":
        return os.path.isdir(path)
    elif path_type == "file":
        return os.path.isfile(path)

def check_saved_path(file, key, path_type):
    ''' Loads path (= value of the given key in the file) and
        checks if it exists as the given path type (directory or file).
    '''
    path = load(file)[key]
    return check_path(path, path_type)

def change_path(file, key, new_path, path_type):
    ''' Reads path from file (as the value of the given key) and change it to new_path.
        Checks if the path exists and is of the given path type (directory of file) before changing.
    '''
    if check_path(new_path, path_type) == True:
        loaded_data = load(file)
        loaded_data[key] = new_path
        with open(file, 'w') as f:
            json.dump(loaded_data, f)
        print('Your new {} is {}.'.format(key, os.path.abspath(new_path)))
    else:
        print('Not a correct path. Please try again.')

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
