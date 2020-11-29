
import article
from lxml import html
import requests


def arxiv(aX_num):
    ''' Ask for arXiv number and return corresponding Article class. '''
    # python 3 truncates leading zeros but these might occur in arxiv identifiers
    aX_num = str(aX_num).zfill(9)
    abs_url = 'https://arxiv.org/abs/{}'.format(aX_num)
    print(abs_url)
    src_abs = requests.get(abs_url)
    # obtain a _structured_ document ("tree") of source of abs_url
    page_tree =  html.fromstring(src_abs.content)
    # extract article data from page_tree (as lists)
    title = page_tree.xpath('//title')[0]
    all_authors = page_tree.xpath('//meta[@name="citation_author"]/@content')
    full_abstract = page_tree.xpath('//meta[@property="og:description"]/@content')
    title_name = title.text_content()
    # create a convenient authors' name
    authors_list = [a.split(', ')[0] for a in all_authors[:3]]
    if len(all_authors) > 3:
        authors_name = authors_list[0] + ' et al'
    elif 1 < len(all_authors) <= 3:
        authors_name = ', '.join(authors_list[:-1])
        authors_name += ' and ' + authors_list[-1]
    else: 
        authors_name = authors_list[0]              # TODO: IMPROVE!?!?
    # convert abstract into nicer string
    full_abstract = page_tree.xpath('//meta[@property="og:description"]/@content')
    abstract_text = ' '.join(full_abstract)

    return article.Article(title = title_name, authors = authors_name, abstract = abstract_text, aX_num = aX_num)


def check(aX_num):
    ''' Helper function to check if arXiv number exists. '''
    abs_url = 'https://arxiv.org/abs/{}'.format(aX_num)
    r = requests.get(abs_url)
    # check status of request
    return r.status_code == requests.codes.ok

















