import article
from dir_control import control_dir
from lxml import html
import requests
import os


def arxiv(ax_id):
    ''' Ask for arXiv identifier and return corresponding Article class. '''
    # python 3 truncates leading zeros but these might occur in arxiv identifiers
    ax_id = str(ax_id).zfill(9)
    abs_url = 'https://arxiv.org/abs/{}'.format(ax_id)
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

    return article.Article(title = title_name, authors = authors_name, abstract = abstract_text, ax_id = ax_id)


def check(ax_id):
    ''' Helper function to check if arXiv identifier exists. '''
    abs_url = 'https://arxiv.org/abs/{}'.format(ax_id)
    r = requests.get(abs_url)
    # check status of request
    return r.status_code == requests.codes.ok
