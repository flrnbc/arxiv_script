import retrieve
from dir_control import control_dir
import click
import subprocess

@click.group()
def cli():
    """ Script to download and show arXiv articles. Version 0.1. """

@cli.command("get")
@click.option("-a", "--abstract", is_flag = True, help="Show abstract of the article. Does _not_ download it.")
@click.option("-o",  "--open-file", is_flag = True, help="Opens the article after download.")
@click.option("-dir", "--directory", default = control_dir('read'), help="Download article to given directory (instead of to the default one).")
@click.argument("ax_id")
def get(ax_id, abstract, open_file, directory):
    ''' Ask for arXiv identifier and download article. '''
    while retrieve.check(ax_id) == False:
        ax_id = str(input("Please enter a valid arXiv identifier (enter 'q' to quit)."))
        if ax_id == 'q':
            break
    else:
        article = retrieve.arxiv(ax_id)
        print("{} \nby {}".format(article.title, article.authors))
        # decided to only print abstract when this flag is given (comes close to 'browsing' articles)
        if abstract:
            print(article.abstract)
        else:
            while control_dir('check') == False:
                control_dir('change')
            else:
                saved_path = article.download(save_dir = directory)
                print("Article saved as {}.".format(saved_path))
                # TODO: needs to be adapted to other os as well!
                if open_file:
                    subprocess.call(["open", saved_path])
