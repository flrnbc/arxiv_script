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
    """ Set default bib-file to which BibTeX-entries are added. """
    if not bib_file or ctx.resilient_parsing:
        return
    if os.path.splitext(bib_file)[1] != ".bib":
        print("Not a correct bib-file. Please try again.")
    else:
        change_path(file = 'data', key = 'bib-file', new_path = bib_file, path_type = 'file')
        # NOTE: here we implicitly catch invalid paths.
    ctx.exit()

# arXiv script
@click.group()
@click.option("--set-directory", expose_value = False, callback = set_download_dir, is_eager = True, help = "Set default directory to which articles are downloaded.")
@click.option("--set-bib-file", expose_value = False, callback = set_bib, is_eager = True, help = "Set default bib-file to which BibTeX entries are added.")
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
    ''' Download the article corresponding to an arXiv identifier. '''
    article = ctx.obj
    print("\n\"{}\" \nby {} \n".format(article.title, article.authors_short))
    if directory == "":
    # TODO: needs to be changed if we rename the script
        print("Please either set a default download directory by using 'arxiv_script --set-directory PATH'\nor use 'arxiv_script AX_ID get -dir PATH'.")
    elif os.path.isdir(directory) == False:
        print('Please give a valid absolute path to a directory.')
    else:
        saved_path = article.download(save_dir = directory)
        print("Article saved as {}.".format(os.path.abspath(saved_path)))
        # TODO: needs to be adapted to other os as well!
        if open_file:
            subprocess.call(["open", saved_path])

@cli.command("show")
@click.option("-f", "--full", is_flag = True, help = "Shows details of article (including all authors and main subject on arXiv).")
@click.pass_context
def show(ctx, full):
    """ Show title, authors and abstract of an arXiv identifier. """
    article = ctx.obj
    if full == False:
        print("\nTitle:\n{} \n\nAuthor(s):\n{} \n\nAbstract:\n{}\n".format(article.title, article.authors_short, article.abstract))
    else:
        print(article)

@cli.command("bib")
@click.option('-add', '--add-to', default = default_bib_file, help = "Path to a bib-file to which the BibTeX entry is added.")
@click.pass_context
def bib(ctx, add_to = default_bib_file):
    ''' Create bibtex entry for an arXiv identifier (optionally add to default or some other bib-file). '''
    article = ctx.obj
    bib_entry = article.bib()
    print(f"\nHere is the requested BibTeX entry:\n\n{bib_entry}\n")
    ctx.obj = bib_entry
    if add_to == "":
        # TODO: needs to be changed if we rename the script
        print("Note: to add the BibTeX entry to a bib-file either set a default bib-file via 'arxiv_script --set-bib-file FILE PATH'\nor use 'arxiv_script AX_ID bib add -to FILE PATH'.")
    elif os.path.splitext(add_to)[1] != ".bib":
        print("The given path does not point to a bib-file. Please try again.")
    elif os.path.isfile(add_to) == False:
        print("The given path is not a valid one. Please try again.")
    else:
        bib_entry = ctx.obj
        if click.confirm("Do you want to add this BibTeX entry to {}?".format(os.path.abspath(add_to))):
            with open(to, 'a') as f:
                f.write("\n{}".format(bib_entry))
                print("BibTeX entry successfully added.")
