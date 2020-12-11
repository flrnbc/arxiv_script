import article
from lxml import html
import requests


def arxiv(ax_id):
    ''' Ask for arXiv number and return corresponding Article class. '''
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
    ''' Helper function to check if arXiv number exists. '''
    abs_url = 'https://arxiv.org/abs/{}'.format(ax_id)
    r = requests.get(abs_url)
    # check status of request
    return r.status_code == requests.codes.ok

def retrieve(opt = "show", ax_id):
    ''' Either ask to print ('show') an article or download ('get') it. '''
    while check(ax_id) == False:
        ax_id = str(input("Please enter a valid arxiv identifier (enter 'q' to quit)."))
        if ax_id == 'q':
            break
    else:
        article = arxiv(ax_id)
        if opt == "show":
            print(article)
        elif opt == "get":
            print(article.title)
            # TODO: add delay before download?
            article.download()
