""" Testing path_control.py """

import os
from dotenv import load_dotenv, find_dotenv, set_key
from src.path_control import check_path


def test_check_path():
    assert check_path("/Users/fbeck/Documents/Math", 
                    "DEFAULT_DIRECTORY") == True
    assert check_path ("/Users/fbeck/Documents/Math2", 
                    "DEFAULT_DIRECTORY") == False
    assert check_path("/Users/fbeck/Documents/Math", 
                    "DEFAULT_BIB_FILE") == False
    assert check_path("/Users/fbeck/Documents/Rise/python/arxiv-script/test.bib", 
                    "DEFAULT_BIB_FILE") == True
    assert check_path("/Users/fbeck/Documents/Rise/python/arxiv-script/script/article.py", 
                    "DEFAULT_BIB_FILE") == False 


## Copied set_default to avoid complications with the two different .env-files 
## (one for testing, the other for the actual script).
def set_default(path, path_type):
    """ 
    Set default directory (path_type = 'DEFAULT_DIRECTORY')
    or default bib file (path_type = 'DEFAULT_BIB_FILE').
    """
    if not check_path(path = path, path_type = path_type): 
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
    



    
