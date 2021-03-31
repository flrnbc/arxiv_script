""" Short tests for retrieve.py """

from src.retrieve import get_year, arxiv, check


def test_get_year():
    assert get_year("cmp-lg/9404002") == "1994"
    assert get_year("hep-th/99032314") == "1999"
    assert get_year("math.GT/020912") == "2002"
    assert get_year("1010.12345") == "2010"


def test_check():
    assert not check("2011:01212")
    assert check("math.GT/0309136")
    assert check("cmp-lg/9404002")
    assert not check("9308.12301")


def test_arxiv():
    # check if arxiv prints correctly (use -s flag in pytest)
    print(arxiv("math.GT/0309136"))
