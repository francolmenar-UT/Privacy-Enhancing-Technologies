import timeit

import click
from pyfiglet import Figlet
from src.constants.const import *
from src.paillier.paillier import key_gen, enc


@click.group()
def main():
    pass


@main.command(help='.')
def pail():
    pk, sk = key_gen()
    # pk.toString()
    # sk.toString()

    msg_enc = enc(MSG, pk)
    print(msg_enc)


@main.command(help='Generates the Graphs from the data')
def graph():
    """
    Generates the Graphs
    """
    # create_graph()
    print("Graph")
    return 0


f = Figlet(font='slant')  # Useless cool text
print(f.renderText('Paillier'))

main()  # Runs the cli
