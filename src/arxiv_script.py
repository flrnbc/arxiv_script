"""Main code for the script mainly using Click
(see https://palletsprojects.com/p/click/
for details, in particular on the use of callback
functions).
"""

import os
import subprocess

import click
from dotenv import find_dotenv, load_dotenv

import src.retrieve as retrieve
from src.path_control import check_path, get_opener, set_default

# load environment variables from local .env-file
# also used for help to show the default directory/bib file.
# hence we already load it here.
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


# callback functions to set default download directory and bib file.
def set_download_dir(ctx, param, directory):
    """Set default directory where articles are downloaded to.
    Note: 'param' is not used here but required by Click."""
    # the following ensures that the parameters for --set-directory
    # are passed to this function
    if not directory or ctx.resilient_parsing:
        return
    set_default(path=directory, path_type="dir")
    ctx.exit()


def set_bib(ctx, param, bib_file):
    """Set default bib-file to which BibTeX-entries are added.
    Again, param is not used here but required by Click."""
    if not bib_file or ctx.resilient_parsing:
        return
    set_default(path=bib_file, path_type="bib")
    ctx.exit()


######################
# arXiv script (axs) #
######################
@click.group()
@click.option(
    "--set-directory",
    expose_value=False,
    callback=set_download_dir,
    is_eager=True,
    help="Set default directory to which articles are downloaded."
    + "\nDefault: {}".format(os.getenv("DEFAULT_DIRECTORY")),
)
@click.option(
    "--set-bib-file",
    expose_value=False,
    callback=set_bib,
    is_eager=True,
    help="Set default bib-file to which BibTeX entries are added."
    + "\nDefault: {}".format(os.environ["DEFAULT_BIB_FILE"]),
)
def cli():
    """Script to download & show arXiv articles and create a bibtex entry
    for them. Version 0.2.
    """


@cli.command("get")
@click.option(
    "-o", "--open-file", is_flag=True, help="Opens the article after download."
)
# envvar below ensures that the default of 'directory' is the environment
# variable 'DEFAULT_DIR'.
@click.option(
    "-d",
    "--directory",
    envvar="DEFAULT_DIRECTORY",
    help="Download article to given directory" + "(instead to the default one).",
)
@click.argument("ax_id")
def get(ax_id, open_file, directory):
    """Download the article corresponding to an arXiv identifier."""
    article = retrieve.arxiv(ax_id)
    if not article:
        return 1

    print(f'\n"{article.title}" \nby {article.authors_short}\n')
    if not directory:
        print(
            "Please either set a default download directory by using"
            + "'axs --set-directory PATH'\n"
            + "or use 'axs AX_ID get -d PATH'."
        )
        return 1

    if not check_path(directory, "dir"):
        print("Please give a valid (absolute) path to a directory.")
        return 1

    saved_path = article.download(save_dir=directory)
    print(f"Article saved as {saved_path}.")
    if open_file:
        opener = get_opener()
        subprocess.call([f"{opener}", saved_path])
    return 0


@cli.command("show")
@click.option(
    "-f",
    "--full",
    is_flag=True,
    help="Shows details of article"
    + " (including all authors and main subject on arXiv).",
)
@click.argument("ax_id")
def show(ax_id, full):
    """Show title, authors and abstract of an arXiv identifier."""
    article = retrieve.arxiv(ax_id)
    if not article:
        return 1

    if not full:
        print(
            f"\nTitle:\n{article.title}\n\n"
            f"Author(s):\n{article.authors_short}\n\n"
            f"Abstract:\n{article.abstdact}\n"
        )
        return 0

    print(article)
    return 0


@cli.command("bib")
@click.option(
    "-a",
    "--add-to",
    envvar="DEFAULT_BIB_FILE",
    help="Path to a bib-file to which the BibTeX entry is added.",
)
@click.argument("ax_id")
def bib(ax_id, add_to):
    """Create bibtex entry for an arXiv identifier."""
    article = retrieve.arxiv(ax_id)
    if not article:
        return 1

    bib_entry = article.bib()
    print(f"\nHere is the requested BibTeX entry:\n\n{bib_entry}\n")

    if not add_to:
        print(
            "Please either set a default bib-file ('axs --set-bib-file`)"
            + "\nor give a valid path to a bib-file."
        )
        return 1

    if not check_path(add_to, "bib"):
        print("The given path does not point to a valid bib-file. Please try again.")
        return 1

    with open(add_to, "a") as file:
        file.write(bib_entry)
        print(f"BibTeX entry successfully added to {add_to}.")
    return 0
