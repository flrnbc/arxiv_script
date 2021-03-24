"""
Main code for the script mainly using Click
(see https://palletsprojects.com/p/click/
for details, in particular on the use of callback
functions).
"""

import os
import subprocess
import click
from dotenv import find_dotenv, load_dotenv
from script.path_control import set_default, get_opener
import script.retrieve as retrieve


# callback functions to set default download directory and bib file.
def set_download_dir(ctx, directory):
    """ Set default directory where articles are downloaded to. """
    # the following ensures that the parameters for --set-directory
    # are passed to this function
    if not directory or ctx.resilient_parsing:
        return
    set_default(path = directory, path_type="DEFAULT_DIRECTORY")
    ctx.exit()


def set_bib(ctx, bib_file):
    """ Set default bib-file to which BibTeX-entries are added. """
    if not bib_file or ctx.resilient_parsing:
        return
    set_default(path = bib_file, path_type="DEFAULT_BIB_FILE")
    ctx.exit()


########################
## arXiv script (axs) ##
########################
@click.group()
@click.option("--set-directory", expose_value = False,
              callback = set_download_dir,
              is_eager = True,
              help = "Set default directory to which articles are downloaded.")
@click.option("--set-bib-file", expose_value = False,
              callback = set_bib,
              is_eager = True,
              help = "Set default bib-file to which BibTeX entries are added.")
def cli():
    """ 
    Script to download & show arXiv articles and create a bibtex entry
    for them. Version 0.1.
    """
    # load environment variables from local .env-file
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)


@cli.command("get")
@click.option("-o",  "--open-file", is_flag = True,
              help = "Opens the article after download.")
# envvar below ensures that the default of 'directory' is the environment
# variable 'DEFAULT_DIR'.
@click.option("-d", "--directory",
              envvar="DEFAULT_DIRECTORY",
              help = "Download article to given directory" +
                     "(instead to the default one).")
@click.argument('ax_id')
def get(ax_id, open_file, directory):
    """ Download the article corresponding to an arXiv identifier. """
    article = retrieve.arxiv(ax_id)
    if article:
        print("\n\"{}\" \nby {}\n".format(article.title, article.authors_short))
        # TODO: if the 'DEFAULT_DIR = ""', then 'directory' seems to be None.
        if directory in ("", None):
            print("Please either set a default download directory by using"
                  + "'axs --set-directory PATH'\n" +
                  "or use 'axs AX_ID get -d PATH'.")
        elif os.path.isdir(directory) is False:
            print('Please give a valid absolute path to a directory.')
        else:
            # download article and show the download path
            saved_path = os.path.abspath(article.download(save_dir = directory))
            print("Article saved as {}.".format(saved_path))
            if open_file:
                opener = get_opener()
                subprocess.call([f"{opener}", saved_path])


@cli.command("show")
@click.option("-f", "--full", is_flag = True, help = "Shows details of article"
              + " (including all authors and main subject on arXiv).")
@click.argument('ax_id')
def show(ax_id, full):
    """ Show title, authors and abstract of an arXiv identifier. """
    article = retrieve.arxiv(ax_id)
    if article:
        if not full:
            print("\nTitle:\n{} \n\nAuthor(s):\n{} \n\nAbstract:\n{}\n"
                  .format(article.title, article.authors_short, article.abstract))
        else:
            print(article)


@cli.command("bib")
@click.option('-a', '--add-to', envvar="DEFAULT_BIB_FILE",
              help = "Path to a bib-file to which the BibTeX entry is added.")
@click.argument('ax_id')
def bib(ax_id, add_to):
    """ Create bibtex entry for an arXiv identifier. """
    article = retrieve.arxiv(ax_id)
    if article:
        bib_entry = article.bib()
        print(f"\nHere is the requested BibTeX entry:\n\n{bib_entry}\n")
        # TODO: again need to treat the 'None case'...
        if add_to in ("", None):
            print("Note: to automatically add the BibTeX entry to a bib-file"
                  + "\neither set a default bib-file via 'axs"
                  + " --set-bib-file FILE PATH'"
                  + "\nor use 'axs AX_ID bib -a FILE PATH'.")
        elif os.path.splitext(add_to)[1] != ".bib":
            print("The given path does not point to a bib-file. Please try again.")
        elif not os.path.isfile(add_to):
            print("The given path is not a valid one. Please try again.")
        else:
            if click.confirm("Do you want to add this BibTeX entry to {}?". 
                             format(os.path.abspath(add_to))):
                with open(add_to, 'a') as file:
                    file.write("\n{}".format(bib_entry))
                    print("BibTeX entry successfully added.")
