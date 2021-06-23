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
    return 1


def set_default(path, path_type):
    """Set default directory (path_type = 'dir')
    or default bib file (path_type = 'bib').
    """
    if not check_path(path=path, path_type=path_type):
        print("Not a correct path. Please try again.")
    else:
        # load .env-file for environment variables
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        # set the environment variable (in current session)
        if path_type == "dir":
            env_var = "DEFAULT_DIRECTORY"
        elif path_type == "bib":
            env_var = "DEFAULT_BIB_FILE"
        os.environ[env_var] = path
        # set it in the dot-file (performed only after the session)
        set_key(dotenv_file, env_var, path)
        # for better printing
        env_var_print = env_var.replace("_", " ")
        print(f"New {env_var_print.lower()} has been set.")


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
