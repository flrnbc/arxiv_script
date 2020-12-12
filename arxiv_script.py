import retrieve
from dir_control import control_dir
import click


@click.group()
def cli():
    """Script to download and show arXiv articles. Version 0.1."""

@cli.command("get")
#@click.option("--dir")
@click.argument("ax_id")
def get(ax_id):
    retrieve.get(ax_id)
