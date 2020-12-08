
import retrieve
import click

@click.group()
def cli():
    """Script to download and show arXiv articles. Version 0.1."""

@cli.command("get")
@click.option("--dir")
@click.argument("ax_id")
def get_article(ax_id):
    """Download article with arXiv identifier ax_id."""
    while retrieve.check(ax_id) == False:
        ano = str(input("Please enter a valid arxiv identifier (enter 'q' to quit)."))
        if ax_id  == 'q':
            break
    else: 
        article = retrieve.arxiv(ax_id)
        print(article)

@cli.command("show")
@click.argument("ax_num")
def show_article(ax_num):
    pass

 



