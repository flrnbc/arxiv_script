
from lxml import html
import requests
import os
import json

## FUNCTION to set directory for saving articles
def save_dir(change = ""):
    with open('data', mode='r') as f:
        # here it's ok to work with only one dict
        # however, it's not the most efficient way because we copy parts of the dict which does not change
        save_data = json.load(f)
        save_dir = save_data["save_dir"]
    if save_dir == "" or change == "cd":
        new_save_dir = ""
        # check if path exists
        while os.path.exists(new_save_dir) == False: 
            new_save_dir = str(input("Please enter a valid absolute directory path where you want to save your arXiv preprints."))
            # TODO: so far only for macOS; also need win!
        else: 
            save_data["save_dir"] = new_save_dir
            with open('data', 'w') as f:
                json.dump(save_data, f)
            print("Your articles will now be downloaded to {}.".format(new_save_dir))
            return save_data["save_dir"] 

## ARTICLE CLASS
# separated it from arxiv() to allow for sources other than arxiv (later...)
# meta_data: for now just arxiv-number

class Article:
    def __init__(self, title, authors, abstract, meta_data):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.meta_data = meta_data

    def __str__(self):
        return f"Title:\n{self.title} \nAuthors:\n{self.authors} \nAbstract:\n{self.abstract} \nMeta data:\n{self.meta_data}"

    def download(self):
        with open('data', 'r') as f:
            save_data = json.load(f)
            save_directory = save_data["save_dir"]
        while True: 
            download_yn = input("Do you want to download the article {}? (y/n) \n(Enter 'cd' if you want to change the directory.)".format(self.title))
            if download_yn == "cd":
                save_directory = save_dir("cd")
                continue
            elif download_yn == "y":
                # create file name 
                file_name = self.authors + " - " + self.title
                # request the pdf url
                pdf_url = 'https://arxiv.org/pdf/{}.pdf'.format(self.meta_data)
                r_pdf = requests.get(pdf_url)
                # download file
                open('{}/{}.pdf'.format(save_directory, file_name), 'wb').write(r_pdf.content)
                return "File saved as \n {}/{}.pdf".format(save_directory, file_name)
            elif download_yn == "n":
                return "No download."
            else: 
                print("Please enter y (yes), n (no) or cd (change directory).")
                continue

## FUNCTION asking for arxiv identifier, returns authors etc. 
def arxiv():
    while True: 
        try: 
            arxiv_num = input("Which arxiv preprint do you want to look at? Please enter the arxiv identifier.")
            # request source code of webpages
            abs_url = 'https://arxiv.org/abs/{}'.format(arxiv_num)
            src_abs = requests.get(abs_url)
            # obtain a structured document ("tree") of r_url
            page_tree =  html.fromstring(src_abs.content)
            # extract title, authors, abstract from page_tree (as list)
            title = page_tree.xpath('//title')[0]
            all_authors = page_tree.xpath('//meta[@name="citation_author"]/@content')
            full_abstract = page_tree.xpath('//meta[@property="og:description"]/@content')
            # convert to convenient strings
            title_name = title.text_content()
            # create a convenient authors' name
            authors_list = [a.split(', ')[0] for a in all_authors[:3]]

            if len(all_authors) > 3:
                authors_name = authors_list[0] + ' et al'
            elif 1 < len(all_authors) <= 3:
                authors_name = ', '.join(authors_list[:-1])
                authors_name += ' and ' + authors_list[-1]
            else: 
                authors_name = authors_list[0]              # IMPROVE!?!?

            full_abstract = page_tree.xpath('//meta[@property="og:description"]/@content')
            abstract_text = ' '.join(full_abstract)
            return Article(title = title_name, authors = authors_name, abstract = abstract_text, meta_data = arxiv_num)
        
        except: 
            print("Not a correct arxiv identifier. Please try again.")
            continue

#############
## PROGRAM ##
#############

while True: 
    save_dir()
    article = arxiv()
    print(article)
    print(article.download())
    new_download = input("Do you want to download another arxiv preprint? (y/n)")

    if new_download == "y":
        continue
    elif new_download == "n":
        print("Happy reading!")
        break
    else: 
        print("Please enter y (yes) or n (no).")
        continue
















