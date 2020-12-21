from lxml import html
from path_control import load
import requests
import time

## article class
# add some meta-data?

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
        bib_entry = "@article{{{0},\n\tAuthor = {{{1}}},\n\tTitle = {{{2}}},\n\tNote = {{\\href{{{3}}}{{arXiv:{4}}}}},\n}}".format(tag, self.authors, self.title, url, self.ax_id)
        print(bib_entry)
