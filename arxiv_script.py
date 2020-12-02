
import retrieve
import click

@click.command()
#@click.option('--ano', default=0))
@click.argument('ano', type=str, default=0)
def cli(ano):    
    ''' Script to download arXiv articles. '''
    while retrieve.check(ano) == False:
        print('Too bad!')
        ano = input("Please enter a valid arxiv identifier.")
        ano = ano.zfill(9)
    else: 
        article = retrieve.arxiv(ano)
        print(article)

#a_no = input('Give me a valid arxiv identifier.')
#cli(a_no)
