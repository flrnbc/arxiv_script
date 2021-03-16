""" Short tests for retrieve.py """

from script.retrieve import get_year
from script.retrieve import arxiv

# tests
def test_get_year():
    assert get_year("cmp-lg/9404002") == "1994"
    assert get_year("hep-th/99032314") == "1999"
    assert get_year("mathGT/00112314") == "2000"
    assert get_year("1010.12345") == "2010"

#def test_arxiv():
#    print(arxiv('1308.2198'))
#    print(arxiv('hep-th/0002138'))

#print(test_get_year())
#test_arxiv()
