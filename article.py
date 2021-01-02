from lxml import html
from path_control import load
import requests
import re
import time

# helper function(s)
def escape_special_chars(string, special_chars):
    """ Escpae special characters via adding backslash. """
    escape_string = string
    for ss in special_chars:
        escape_string = re.sub(ss, '\\' + ss, escape_string)
    return escape_string

def bib_title(string):
    """ Helper function to create correct title for bibtex, i.e. curly braces around captial words
        to actually print them in captial and escaping special characters.
    """
    caps = re.compile("[A-Z]")
    special = [r'"', r'{', r'}']
    split_string = string.split()
    split_string = [escape_special_chars(w, special) for w in split_string]
    split_string = ["{{{}}}".format(w) if re.search(caps, w) else w for w in split_string]
    return ' '.join(split_string)


# article class
class Article:
    """ Class for articles. All attributes are self-explanatory except for
        - authors_short: short version of the authors' names which is used to save an article or create a bibtex key.
          Formate (as created via retrieve.py):
          2 authors: A and B.
          3 authors: A, B and C.
          > 3 authors: A et al.
        - ax_id: short for arxiv identifier.
        - main_subject: main arxiv subject.
    """
    def __init__(self, title, authors, authors_short, abstract, ax_id, year, main_subject):
        self.title = title
        self.authors = authors
        self.authors_short = authors_short
        self.abstract = abstract
        self.ax_id = ax_id
        self.year = year
        self.main_subject = main_subject

    def __str__(self):
        return f"Title:\n{self.title} \n\nAuthors:\n{self.authors}\n\nAbstract:\n{self.abstract} \n\narXiv identifier:\n{self.ax_id} \n\nYear: \n{self.year} \n\nMain subject: \n{self.main_subject}"

    default_directory = load('data')['default directory']
    default_bib = load('data')['bib-file']

    def download(self, save_dir = default_directory):
        """ Download article to save_dir. """
        file_name = self.authors_short + '-' + self.year + '-' + self.title
        # request url of pdf
        pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.ax_id)
        r_pdf = requests.get(pdf_url)
        # download file with delay
        print("Preparing download... (press Ctrl + c to cancel)")
        time.sleep(3)
        open('{}/{}.pdf'.format(save_dir, file_name), 'wb').write(r_pdf.content)
        return "{}/{}.pdf".format(save_dir, file_name)

    def bib_key(self):
        """ Create a convenient bibtex entry.
            For authors: `Contract' the short authors' name, i.e. remove white space and capitalize 'et al' (if present).
            For title: Remove commas as well as all common proposition and articles (i.e. 'on', 'in', 'a', 'the', ...);
            then take the first three words.
        """
        # key for authors
        # NOTE: somewhat `hacky` and inefficient because we already implicitly generate a list of authors when retrieving the article
        # TODO: what about accents? E.g. in d'Angolo or French accents etc.
        if re.search(r',', self.authors_short) == None:
            authors_key = re.sub(r' et al', r'EtAl', self.authors_short)    # only necessary > 3 authors
            re.sub(r'\s', '', authors_key)    # NOTE: there might be names like "de ..."
        else:
        ## remove ',' as well as 'and' if there are more authors
            authors_short_list = re.sub(r'and\b|,', '', self.authors_short)
            authors_key = ''.join(a[0] for a in authors_short_list)
        # key for title
        title_key = re.sub(r'of\b|a\b|the\b|in\b|on\b|,', '', self.title)
        title_key_split = title_key.split()
        title_key = ''.join(t.capitalize() for t in title_key_split[:3])
        return authors_key + "_" + title_key + "_" + self.ax_id    # TODO: add arxiv identifier only to make key unique --> better way?


    def bib(self):#, bib_file = default_bib):
        """ Create a bibtex entry for the given article using bib_key and bib_tile. """
        article_key = self.bib_key()
        url = "https://arxiv.org/abs/{}".format(self.ax_id)
        title = bib_title(self.title)
        bib_entry = "@article{{{0},\n\tAuthor = {{{1}}},\n\tTitle = {{{2}}},\n\tYear = {{{3}}},\n\tNote = {{\\href{{{4}}}{{arXiv:{5}}}}}\n}}".format(article_key, self.authors, title, self.year, url, self.ax_id)
        return bib_entry


# tests
def test_bib_title():
    test_string = "A crucial input to the Geometry of the Universe, the Quasar-CMB and its relation to mRNA and the $\zeta$-function. Morever, some brackets { { } can not hurt either."
    print(bib_title(test_string))

def test_escape():
    test_string = r'Here is a lonlely bracket { and here is another one }. Now comes " and }.'
    print(escape_special_chars(test_string, special_chars = [r"[{}]"]))

#test_bib_title()
#test_escape()
