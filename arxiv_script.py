import retrieve
from dir_control import control_dir
import click


@click.group()
def cli():
    """Script to download and show arXiv articles. Version 0.1."""

@cli.command("get")
#@click.option("--dir")
@click.argument("ax_id")
def get_article(ax_id):
    """Download article with arXiv identifier ax_id."""
    while control_dir("check") == False:
        control_dir("change")
    else:
        article = show_article(ax_id)
        print(article)
        article.download()

@cli.command("show")
@click.argument("ax_id")
def show_article(ax_id):
    while retrieve.check(ax_id) == False:
        ax_id = str(input("Please enter a valid arxiv identifier (enter 'q' to quit)."))
        if ax_id  == 'q':
            break
    else:
        article = retrieve.arxiv(ax_id)
        print(article)
