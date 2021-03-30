""" Testing path_control.py """

import os
from dotenv import load_dotenv, find_dotenv, set_key
from src.path_control import check_path


def test_check_path():
    test_dir = os.getcwd() + "/tests/test_directory"
    test_bib = test_dir + "/test.bib"
    test_article = os.getcwd() + "/test_article.py"
    assert check_path(test_dir, "DEFAULT_DIRECTORY")
    assert not check_path(test_bib, "DEFAULT_DIRECTORY")
    assert not check_path("/nothing/is/here", "DEFAULT_DIRECTORY")

    assert check_path(test_bib, "DEFAULT_BIB_FILE")
    assert not check_path(test_dir, "DEFAULT_BIB_FILE")
    assert not check_path(test_article, "DEFAULT_BIB_FILE")


# Copied set_default to avoid complications with the two different .env-files
# (one for testing, the other for the actual script).
def set_default(path, path_type):
    """ Set default directory (path_type = 'DEFAULT_DIRECTORY')
    or default bib file (path_type = 'DEFAULT_BIB_FILE').
    """
    if not check_path(path=path, path_type=path_type):
        print("Not a correct path. Please try again.")
    else:
        # load .env-file for environment variables
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file)
        # set the environment variable (= path_type)
        set_key(dotenv_file, path_type, path)
        print(os.getenv("DEFAULT_DIRECTORY"))
        # for better printing
        env_var_print = path_type.replace("_", " ")

        print("New {} has been set.".format(env_var_print.lower()))

############################################
## test does NOT WORK because environment ##
## variables are not instantly updated.   ##
############################################

# def test_set_default():
#     dotenv_file = find_dotenv()
#     load_dotenv(dotenv_file)

#     set_default("/Users/fbeck/Documents/", "DEFAULT_DIRECTORY")
#     assert os.getenv("DEFAULT_DIRECTORY") == "/Users/fbeck/Documents/"

#     # see if it rejects invalid directory paths
#     set_default("/Users/fbeck/Docs/", "DEFAULT_DIRECTORY")
#     assert os.getenv("DEFAULT_DIRECTORY") == "/Users/fbeck/Documents/"

#     test_bib = "Users/fbeck/Documents/Rise/python/arxiv_script/tests/test.bib"
#     set_default(test_bib, "DEFAULT_BIB_FILE")
#     assert os.getenv("DEFAULT_BIB_FILE") == test_bib

#     set_default("/Users/fbeck/Documents/", "DEFAULT_BIB_FILE")
#     assert os.getenv("DEFAULT_BIB_FILE") == test_bib

#     # reset .env-file
#     set_key(dotenv_file, "DEFAULT_DIRECTORY", "")
#     print(os.getenv("DEFAULT_DIRECTORY"))
#     assert os.getenv("DEFAULT_DIRECTORY") == ""
#     set_key(dotenv_file, "DEFAULT_BIB_FILE", "")
#     assert os.getenv("DEFAULT_BIB_FILE") == ""
