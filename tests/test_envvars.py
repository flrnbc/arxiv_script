""" Test environment variables. """

from script.path_control import check_path
from dotenv import load_dotenv, set_key, find_dotenv
import os

dotenv_file = "/Users/fbeck/Documents/Rise/python/arxiv-script/tests/.env"
load_dotenv(dotenv_file)

def set_download_dir(directory):
    """ Set default directory where articles are downloaded to. """
    if check_path(directory, "directory") == True:
        #os.environ["DEFAULT_DIRECTORY"] = str(directory)
        set_key(dotenv_file, "DEFAULT_DIRECTORY", directory)
        load_dotenv(dotenv_file)
        print('Your new default directory is {}.'.format(os.path.abspath(os.getenv("DEFAULT_DIRECTORY"))))
    else:
        print('Not a correct path. Please try again.')
    #change_path(file = 'script/data', key = 'default directory', new_path = directory, path_type = "dir")

def test_envvars():
    set_download_dir("/Users/fbeck/Documents/Math")
    # problem: is not updated instantly because envvars are tied to the current process
    assert os.getenv("DEFAULT_DIRECTORY") == "/Users/fbeck/Documents/Math"
