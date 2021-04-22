""" Short tests for retrieve.py """

from src.retrieve import arxiv, check, get_year


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
    # check non-existent arxiv identifier
    assert not arxiv("fantasy_ax_id")

    # check existent arxiv identifier
    article = arxiv("math.GT/0309136")
    assert article.title == "Regular points in affine Springer fibers"
    assert article.authors_contracted == "GoreskyKottwitzMacPherson"
    # check if arxiv prints correctly (use -s flag in pytest)
    print(arxiv("math.GT/0309136"))

    # now we check if authors are correctly displayed
    # depending on the number of authors:
    # for one authors
    article2 = arxiv("math/0211159")
    assert article2.authors == "Perelman, Grisha"

    # for > 3 authors
    article3 = arxiv("2104.06383")
    assert article3.authors_contracted == "MarcolongoEtAl"
