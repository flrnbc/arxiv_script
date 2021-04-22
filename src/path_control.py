"""
Helper function to check if path exists
as directory or file. Another helper function
for opening a downloaded file.
"""

import os
import platform

from dotenv import find_dotenv, load_dotenv, set_key


def check_path(path, path_type):
    """Check if path is a directory (path_type = DEFAULT_DIRECTORY)
    or bib-file (path_type = DEFAULT_BIB_FILE).
    Note: the path_type is later on passed to other functions.
    That's we use these names.
    """
    if path_type == "DEFAULT_DIRECTORY":
        return os.path.isdir(path)
    if path_type == "DEFAULT_BIB_FILE":
        return os.path.isfile(path) and os.path.splitext(path)[1] == ".bib"


def set_default(path, path_type):
    """Set default directory (path_type = 'DEFAULT_DIRECTORY')
    or default bib file (path_type = 'DEFAULT_BIB_FILE').
    """
    if not check_path(path=path, path_type=path_type):
        print("Not a correct path. Please try again.")
    else:
        # load .env-file for environment variables
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        # set the environment variable (= path_type) (in current session)
        os.environ[path_type] = path
        # set it in the dot-file (performed only after the session)
        set_key(dotenv_file, path_type, path)
        # for better printing
        env_var_print = path_type.replace("_", " ")

        print("New {} has been set.".format(env_var_print.lower()))


def get_opener():
    """To view a pdf-file, we use subprocess.call(opener, file_path).
    This calls 'opener file_path' as in a terminal and is hence dependent
    on the operating system:
      - OS X: 'opener = open'
      - Win: 'opener = start'
      - Linux based: 'xdg-open'
    """
    osname = platform.system().lower()
    if "windows" in osname:
        opener = "start"
    elif "osx" in osname or "darwin" in osname:
        opener = "open"
    else:
        opener = "xdg-open"
    return f"{opener}"
