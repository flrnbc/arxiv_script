""" Test article.py """

import script.article as sa

def test_escape_special_chars(): 
    chars = [r'"', r"{"]
    test_string = '{here we go "'
    assert sa.escape_special_chars(test_string, chars) == '\\{here we go \\"'


def test_delete_words():
    test1 = "Hello, let's go outside, John!"
    test2 = "This Is All In Capitals."
    to_remove1 = ["John", "outside", "Outside"]
    to_remove2 = ["all", "capitals", "THIS"]
    
    assert sa.delete_words(test1, to_remove1) == "Hello, let's go, !"
    assert sa.delete_words(test2, to_remove2, case_sensitive=False) == "This IS In."

def test_bib_title():
    pass






