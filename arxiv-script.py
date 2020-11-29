
import retrieve
import click

@click.command()
@click.argument(aX_num)
def cli(aX_num):
    ''' Script to download arXiv articles. '''
    while retrieve.check(aX_num) == False: 
        aX_num = str(input("Please enter a valid arxiv identifier."))
        aX_num = aX_num.zfill(9)
    else: 
        article = retrieve.arxiv(aX_num)
        print(article)

