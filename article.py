from lxml import html
from dir_control import control_dir
import requests
import time


## article class
# add some meta-data?

class Article:
    def __init__(self, title, authors, abstract, ax_id):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.ax_id = ax_id

    def __str__(self):
        return f"Title:\n{self.title} \nAuthors:\n{self.authors} \nAbstract:\n{self.abstract} \narXiv number:\n{self.ax_id}"

    def download(self, save_dir = control_dir('read')):
        file_name = self.authors + ' - ' + self.title
        # request url of pdf
        pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.ax_id)
        r_pdf = requests.get(pdf_url)
        # download file
        print("Prepare to download... (press Ctrl + c to cancel)")
        time.sleep(3)
        open('{}/{}.pdf'.format(save_dir, file_name), 'wb').write(r_pdf.content)
        print("Article saved as \n {}/{}.pdf".format(save_dir, file_name))
