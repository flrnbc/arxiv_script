import retrieve
from path_control import load, change_path, check_saved_path
import click
import subprocess
import os

default_directory = load('data')['default directory']
default_bib_file = load('data')['bib-file']

@click.group()
def cli():
    """ Script to download, show arXiv articles and create a bibtex entry for them. Version 0.1. """

@cli.command("get")
@click.option("-o",  "--open-file", is_flag = True, help = "Opens the article after download.")
@click.option("-dir", "--directory", default = default_directory, help = "Download article to given directory (instead of to the default one).")
@click.argument("ax_id")
def get(ax_id, open_file, directory):
    ''' Ask for arXiv identifier and download, show abstract or create a bibtex entry article. '''
    if retrieve.check(ax_id) == False:
        print("Not a correct arXiv identifier, please try again.")
    else:
        article = retrieve.arxiv(ax_id)
        print("{} \nby {} \n".format(article.title, article.authors_short))
        # decided to only print abstract when this flag is given (comes closer to 'browsing' articles)
        if default_directory == "":
            # TODO: needs to be changed if we rename the script
            print("Please either set a default download directory by using 'arxiv_script set -dir'\nor use 'arxiv_script get -dir PATH'.")
        elif os.path.isdir(directory) == False:
            print('Please give a valid absolute path to a directory.')
        else:
            saved_path = article.download(save_dir = directory)
            print("Article saved as {}.".format(saved_path))
            # TODO: needs to be adapted to other os as well!
            if open_file:
                subprocess.call(["open", saved_path])

@cli.command("show")
@click.argument("ax_id")
## TODO: add option to show 'full' article
def show(ax_id):
    """" Show title, (all) authors and abstract of article. """
    if retrieve.check(ax_id) == False:
        print("Not a correct arXiv identifier, please try again.")
    else:
        article = retrieve.arxiv(ax_id)
        print("\nTitle: {} \nAuthor(s): {} \n\nAbstract:\n{}".format(article.title, article.authors, article.abstract))

@cli.command("bib")
@click.argument("ax_id")
## TODO: add option to append bibtex entry
def bib(ax_id):
    ''' Create bibtex entry for the article. '''
    if retrieve.check(ax_id) == False:
        print("Not a correct arXiv identifier, please try again.")
    else:
        article = retrieve.arxiv(ax_id)
        print("\nBibTeX entry for this article:\n\n{}".format(article.bib()))


@cli.group()
def default():
    """ Set default directory for downloads and default bib-file to append BibTeX entries. """

@default.command("dir")
@click.argument("directory")
def set_download_dir(directory):
    """ Set default directory where articles are downloaded to. """
    change_path(file = 'data', key = 'default directory', new_path = directory, path_type = "dir")

@default.command("bib")
@click.argument("bib-file")
def set_bib_file(bib_file):
    change_path(file = 'data', key = 'bib-file', new_path = bib_file, path_type = 'file')


#@cli.command("bib")
#def
