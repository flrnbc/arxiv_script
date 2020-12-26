from lxml import html
from path_control import load
import requests
import time

# helper function(s)
def bib_title(string):
    """ Helper function to create correct title for bibtex, i.e. curly braces around captial words
        to actually print them in captial.
    """
    split_string = string.split()
    split_string = ["{{{}}}".format(w) if w[0] == w[0].capitalize() else w for w in split_string]
    return ' '.join(split_string)




# article class
class Article:
    def __init__(self, title, authors, abstract, ax_id, year, main_subject):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.ax_id = ax_id
        self.year = year
        self.main_subject = main_subject

    def __str__(self):
        return f"Title:\n{self.title} \n\nAuthors:\n{self.authors}\n\nAbstract:\n{self.abstract} \n\narXiv identifier:\n{self.ax_id} \n\nYear: \n{self.year} \n\nMain subject: \n{self.main_subject}"

    default_directory = load('data')['default directory']
    default_bib = load('data')['bib-file']

    def download(self, save_dir = default_directory):
        file_name = self.authors + ' - ' + self.year + ' - ' + self.title
        # request url of pdf
        pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.ax_id)
        r_pdf = requests.get(pdf_url)
        # download file
        print("Preparing download... (press Ctrl + c to cancel)")
        time.sleep(3)
        open('{}/{}.pdf'.format(save_dir, file_name), 'wb').write(r_pdf.content)
        return "{}/{}.pdf".format(save_dir, file_name)
        #print("Article saved as \n {}/{}.pdf".format(save_dir, file_name))

    def bib(self):#, bib_file = default_bib):
        # TODO: think about tag!
        tag = "{}-{}".format(self.authors, self.ax_id)
        url = "https://arxiv.org/abs/{}".format(self.ax_id)
        title = bib_title(self.title)
        bib_entry = "@article{{{0},\n\tAuthor = {{{1}}},\n\tTitle = {{{2}}},\n\tYear = {{{3}}},\n\tNote = {{\\href{{{4}}}{{arXiv:{5}}}}}\n}}".format(tag, self.authors, title, self.year, url, self.ax_id)
        print(bib_entry)



# tests
def test_bib_title():
    test_string = "A crucial input to the Geometry of the Universe"
    test_string2 = "Quasar-CMB" # seen it was not `embraced` in 2011.01234
    print(bib_title(test_string))
    print(bib_title(test_string2))

#test_bib_title()
