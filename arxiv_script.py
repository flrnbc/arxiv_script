import retrieve
from path_control import load, change_path, check_saved_path
import click
import subprocess
import os

default_directory = load('data')['default directory']
default_bib_file = load('data')['bib-file']

# callback functions to set default  download directory and bib file.
def set_download_dir(ctx, directory):
    """ Set default directory where articles are downloaded to. """
    if not directory or ctx.resilient_parsing:
        return
    change_path(file = 'data', key = 'default directory', new_path = directory, path_type = "dir")
    ctx.exit()

def set_bib(ctx, bib_file):
    if not bib_file or ctx.resilient_parsing:
        return
    change_path(file = 'data', key = 'bib-file', new_path = bib_file, path_type = 'file')
    ctx.exit()


# arxiv script
@click.group()
@click.option("--set-directory", expose_value = False, callback = set_download_dir, is_eager = True)
@click.option("--set-bib-file", expose_value = False, callback = set_bib, is_eager = True)
@click.argument('ax_id')
@click.pass_context
def cli(ctx, ax_id):
    """ Script to download, show arXiv articles and create a bibtex entry for them. Version 0.1. """
    if retrieve.check(ax_id) == False:
        print("Not a correct arXiv identifier. Please try again.")
        ctx.exit()
    else:
        article = retrieve.arxiv(ax_id)
        ctx.obj = article

@cli.command("get")
@click.option("-o",  "--open-file", is_flag = True, help = "Opens the article after download.")
@click.option("-dir", "--directory", default = default_directory, help = "Download article to given directory (instead to the default one).")
@click.pass_context
def get(ctx, open_file, directory = default_directory):
    ''' Downloads the article of an arXiv identifier. '''
    article = ctx.obj
    print("{} \nby {} \n".format(article.title, article.authors_short))
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
@click.option("-f", "--full", is_flag = True, help = "Shows details of article (including all authors and main subject on arXiv).")
@click.pass_context
def show(ctx, full):
    """" Show title, authors and abstract of article. """
    article = ctx.obj
    if full == False:
        print("\nTitle:\n{} \n\nAuthor(s):\n{} \n\nAbstract:\n{}\n".format(article.title, article.authors_short, article.abstract))
    else:
        print(article)


@cli.command("bib")
#@click.option("-add", "--add-to-bibfile", is_eager = True, callback = add_bib, expose_value = False)
@click.pass_context
## TODO: add option to append bibtex entry
def bib(ctx):
    ''' Create bibtex entry for the article. '''
    article = ctx.obj
    print(f"\n{article.bib()}\n")
