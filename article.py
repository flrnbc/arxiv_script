from lxml import html
from dir_control import control_dir
import requests


## article class
# add some meta-data?

class Article:
    def __init__(self, title, authors, abstract, aX_num):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.aX_num = aX_num

    def __str__(self):
        return f"Title:\n{self.title} \nAuthors:\n{self.authors} \nAbstract:\n{self.abstract} \narXiv number:\n{self.aX_num}"

    def download(self):
        save_dir = control_dir('read')
        file_name = self.authors + ' - ' + self.title
        # request url of pdf
        pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.aX_num)
        r_pdf = requests.get(pdf_url)
        # download file
        open('{}/{}.pdf'.format(save_dir, file_name), 'wb').write(r_pdf.content)
        return "File saved as \n {}/{}.pdf".format(save_dir, file_name)
