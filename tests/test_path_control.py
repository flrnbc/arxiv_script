""" Testing path_control.py """

import os

import pytest
from dotenv import load_dotenv, set_key

from src.path_control import check_path, get_opener, set_default

# directory/file paths needed for testing
working_dir = os.getcwd()
test_dir = working_dir + "/tests/test_directory"
test_bib = test_dir + "/test.bib"

# load dotenv-file from src/
dotenv_file = working_dir + "/src/.env"
load_dotenv(dotenv_file)


def test_check_path():
    test_article = working_dir + "/test_article.py"
    assert check_path(test_dir, "dir")
    assert not check_path(test_bib, "dir")
    assert not check_path("/nothing/is/here", "dir")

    assert check_path(test_bib, "bib")
    assert not check_path(test_dir, "bib")
    assert not check_path(test_article, "bib")
    assert not check_path("fantasy.bib", "bib")


def test_set_default():
    current_default_dir = os.getenv("DEFAULT_DIRECTORY")
    current_default_bib_file = os.getenv("DEFAULT_BIB_FILE")

    # change DEFAULT_DIRECTORY temporarily
    set_default(test_dir, "dir")
    assert os.getenv("DEFAULT_DIRECTORY") == test_dir

    # see if it rejects invalid directory paths
    with pytest.raises(FileNotFoundError):
        set_default("/not/a/valid/path", "dir")
    assert os.getenv("DEFAULT_DIRECTORY") == test_dir

    # change DEFAULT_BIB_FILE temporarily
    set_default(test_bib, "bib")
    assert os.getenv("DEFAULT_BIB_FILE") == test_bib

    with pytest.raises(FileNotFoundError):
        set_default("/not/a/valid/bib_file", "bib")
    assert os.getenv("DEFAULT_BIB_FILE") == test_bib

    # reset .env-file (for next session)
    set_key(dotenv_file, "DEFAULT_DIRECTORY", current_default_dir)
    set_key(dotenv_file, "DEFAULT_BIB_FILE", current_default_bib_file)


def test_get_opener():
    opener = get_opener()
    assert opener in ["start", "open", "xdg-open"]
