import retrieve
from path_control import load, change_path, check_saved_path
import click
import subprocess
import os

default_directory = load('data')['default directory']

@click.group()
def cli():
    """ Script to download and show arXiv articles. Version 0.1. """

@cli.command("get")
@click.option("-a", "--abstract", is_flag = True, help = "Show abstract of the article. Does _not_ download it.")
@click.option("-o",  "--open-file", is_flag = True, help = "Opens the article after download.")
@click.option("--bib", is_flag = True, help = "Adds bib-entry of the article to the default bib-file.")
@click.option("-dir", "--directory", default = default_directory, help = "Download article to given directory (instead of to the default one).")
@click.argument("ax_id")
def get(ax_id, abstract, bib, open_file, directory):
    ''' Ask for arXiv identifier and download article. '''
    if retrieve.check(ax_id) == False:
        print("Not a correct arXiv identifier, please try again.")
    else:
        article = retrieve.arxiv(ax_id)
        print("{} \nby {} \n".format(article.title, article.authors))
        # decided to only print abstract when this flag is given (comes closer to 'browsing' articles)
        if abstract:
            print("Abstract: \n{}".format(article.abstract))
        elif bib:
            print(article.bib())
        else:
            if directory == "":
                # TODO: needs to be changed if we rename the script
                print("Please either set a default download directory by using 'arxiv_script set' or use 'arxiv_script get -dir.")
            elif os.path.isdir(directory) == False:
                print('Please give a valid absolute path to a directory.')
            else:
                saved_path = article.download(save_dir = directory)
                print("Article saved as {}.".format(saved_path))
                # TODO: needs to be adapted to other os as well!
                if open_file:
                    subprocess.call(["open", saved_path])

@cli.command("set")
# TODO: is the directory path always `loaded` even if we do not want to change the directory?
@click.option("-dd", "--download-dir", help = "Path to a directory.")
@click.option("-bib", "--bib-file", help = "Path to bib-file.")
def set_download_dir(download_dir, bib_file):
    """ Set default directory where articles are downloaded to. """
    change_path(file = 'data', key = 'default directory', new_path = download_dir, path_type = "dir")

#@cli.command("bib")
#def
