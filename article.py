from lxml import html
from path_control import load
import requests
import re
import time

# helper function(s)
def escape_special_chars(string, special_chars):
    """ Escape special characters via adding backslash. """
    escape_string = string
    for ss in special_chars:
        escape_string = re.sub(ss, '\\' + ss, escape_string)
    return escape_string

def delete_words(string, to_delete, case_sensitive = True):
    """ Delete a list of words from given string. If case_sensitive is False, ignore if words in to_delete are captialized or not. """
    # NOTE: I couldn't find a way to remove e.g. the article 'a' from a string with regex.
    # For example, re.sub(r'a\b', '', str) also replaces 'a' at the end of a word...
    # NOTE however: it doesn't catch the words if they are followed e.g. by a comma.
    # In practise, this should not be a problem though.
    split_string = string.split()
    if case_sensitive == False:
        to_delete_caps = [w.capitalize() for w in to_delete]
        to_delete += to_delete_caps
    for w in to_delete:
        while w in split_string:
            split_string.remove(w)
    return ' '.join(split_string)

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
        - authors_short: short version of the authors' names which is printed before a download
          Formate (as created via retrieve.py):
          2 authors: A and B.
          3 authors: A, B and C.
          > 3 authors: A et al.
        - authors_contracted: essentially remove 'and' as well as all space in authors_short;
          used for file name and bibtex key.
        - ax_id: short for arxiv identifier.
        - main_subject: main arxiv subject.
    """
    def __init__(self, title, authors, authors_short, authors_contracted, abstract, ax_id, year, main_subject):
        self.title = title
        self.authors = authors
        self.authors_short = authors_short
        self.authors_contracted = authors_contracted
        self.abstract = abstract
        self.ax_id = ax_id
        self.year = year
        self.main_subject = main_subject

    def __str__(self):
        return f"\nTitle:\n{self.title} \n\nAuthors:\n{self.authors}\n\nAbstract:\n{self.abstract} \n\narXiv identifier:\n{self.ax_id} \n\nYear: \n{self.year} \n\nMain subject: \n{self.main_subject}\n"

    default_directory = load('data')['default directory']
    default_bib = load('data')['bib-file']

    def download(self, save_dir = default_directory):
        """ Download article to save_dir. """
        # create convenient file name
        title_split = self.title.split()
        title_contracted = '_'.join(title_split[:10]) # more intelligent "cut-off"?
        file_name = self.authors_contracted + '-' + title_contracted + '-' + self.year
        file_path = '{}/{}.pdf'.format(save_dir, file_name)
        # request url of pdf
        pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.ax_id)
        r_pdf = requests.get(pdf_url)
        # download file with delay
        t = 3
        while t:
            print("Download in {} second(s) (press Ctrl + c to cancel).".format(t), end='\r')
            time.sleep(1)
            t -= 1
        open(file_path, 'wb').write(r_pdf.content)
        return file_path

    def bib_key(self):
        """ Create a convenient bibtex entry.
            For authors: `Contract' the short authors' name, i.e. remove white space and capitalize 'et al' (if present).
            For title: Remove commas as well as all common proposition and articles (i.e. 'on', 'in', 'a', 'the', ...);
            then take the first three words.
        """
        # key for authors
        authors_key = self.authors_contracted
        # key for title
        ## remove most common propositions and articles
        to_remove = ['a', 'and', 'in', 'of', 'on', 'or', 'the']
        title_key = delete_words(self.title, to_remove, case_sensitive = False)
        print(title_key)
        ## remove characters which are not allowed in bibtex key (or unnecessary)
        remove_chars = re.compile(r'[\\{},~#%:"]')
        title_key_split = title_key.split()
        title_key = ''.join(t.capitalize() for t in title_key_split[:3])
        return authors_key + "-" + title_key + "-" + self.ax_id    # TODO: add arxiv identifier only to make key unique --> better way?

    def bib(self):#, bib_file = default_bib):
        """ Create a bibtex entry for the given article using bib_key and bib_tile. """
        article_key = self.bib_key()
        url = "https://arxiv.org/abs/{}".format(self.ax_id)
        title = bib_title(self.title)
        bib_entry = "@article{{{0},\n\tAuthor = {{{1}}},\n\tTitle = {{{2}}},\n\tYear = {{{3}}},\n\tNote = {{\\href{{{4}}}{{arXiv:{5}}}}}\n}}".format(article_key, self.authors, title, self.year, url, self.ax_id)
        return bib_entry
