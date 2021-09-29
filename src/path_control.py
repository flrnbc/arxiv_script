"""Helper function to check if path exists
as directory or file. Another helper function
for opening a downloaded file.
"""

import os
import platform
from pathlib import Path

from dotenv import find_dotenv, load_dotenv, set_key


def check_path(path, path_type):
    """Check if path is a directory (path_type = 'dir')
    or bib-file (path_type = 'bib).
    """
    path_obj = Path(path)
    if path_type == "dir":
        return path_obj.is_dir()
    if path_type == "bib":
        return path_obj.exists() and path_obj.suffix == ".bib"
    raise FileNotFoundError


def set_default(path, path_type):
    """Set default directory (path_type = 'dir')
    or default bib file (path_type = 'bib').
    """
    if not check_path(path=path, path_type=path_type):
        raise FileNotFoundError
    else:
        # load .env-file for environment variables
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        # set the environment variable (in current session)
        # note: set_key writes to the dot-file but the env var
        # is only available in the next session
        if path_type == "dir":
            os.environ["DEFAULT_DIRECTORY"] = path
            set_key(dotenv_file, "DEFAULT_DIRECTORY", path)
        elif path_type == "bib":
            os.environ["DEFAULT_BIB_FILE"] = path
            set_key(dotenv_file, "DEFAULT_BIB_FILE", path)
        # set it in the dot-file (performed only after the session)
        print("New default has been set.")


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
