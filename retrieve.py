import article
from lxml import html
import requests
import os
import re

def get_year(ax_id):
    """ Extract the year from an arXiv identifier (in format YYYY). """
    modern_ax_id = re.compile(r'([0-9]{2})([0-9]{2}).([0-9]+)')
    search_modern = re.search(modern_ax_id, ax_id)
    if search_modern:
        year = '20' + search_modern[1]
    else:
        old_ax_id = re.compile(r'([a-zA-Z]+[-]?[a-zA-Z]+)/([0-9]{2})([0-9]+)')
        search_old = re.search(old_ax_id, ax_id)
        # get century right
        if search_old[2][0] == "9":
            year = '19' + search_old[2]
        else:
            year = '20' + search_old[2]
    return year


def arxiv(ax_id):
    ''' Ask for arXiv identifier and return corresponding Article class. '''
    # python 3 truncates leading zeros but these might occur in arxiv identifiers
    ax_id = str(ax_id).zfill(9)
    article_year = get_year(ax_id)
    abs_url = 'https://arxiv.org/abs/{}'.format(ax_id)
    src_abs = requests.get(abs_url)
    # obtain a _structured_ document ("tree") of source of abs_url
    page_tree =  html.fromstring(src_abs.content)

    # extract title and abstract from page tree
    title = ' '.join(page_tree.xpath('//meta[@name="citation_title"]/@content'))
    abstract = ' '.join(page_tree.xpath('//meta[@property="og:description"]/@content'))

    # get main subject from page tree
    main_subject = page_tree.xpath('//span [@class="primary-subject"]')[0].text_content()

    # create a convenient authors' name
    all_authors = page_tree.xpath('//meta[@name="citation_author"]/@content')
    authors_list = [a.split(', ')[0] for a in all_authors[:3]]
    if len(all_authors) > 3:
        authors_name = authors_list[0] + ' et al'
    elif 1 < len(all_authors) <= 3:
        authors_name = ', '.join(authors_list[:-1])
        authors_name += ' and ' + authors_list[-1]
    else:
        authors_name = authors_list[0]              # TODO: IMPROVE!?!?

    return article.Article(title = title, authors = authors_name, abstract = abstract, ax_id = ax_id, year = article_year, main_subject = main_subject)


def check(ax_id):
    ''' Helper function to check if arXiv identifier exists. '''
    abs_url = 'https://arxiv.org/abs/{}'.format(ax_id)
    r = requests.get(abs_url)
    # check status of request
    return r.status_code == requests.codes.ok

# short tests
def test_get_year():
    # print(get_year("hep-th/99032314"))
    assert get_year("hep-th/99032314") == "1999"
    assert get_year("mathGT/00112314") == "2000"
    assert get_year("1010:12345") == "2010"
    return "tests pass!"

#print('1308.2198'.zfill(9))

def test_arxiv():
    print(arxiv('1308.2198'))
    print(arxiv('hep-th/0002138'))

#print(test_get_year())
test_arxiv()
