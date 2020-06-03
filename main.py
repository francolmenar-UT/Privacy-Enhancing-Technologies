import timeit

import click
from pyfiglet import Figlet
from src.constants.const import *
from src.paillier.paillier import *


@click.group()
def main():
    pass


@main.command(help='Run the Paillier Encryption')
def pail():
    pk, sk = key_gen()

    # pk.toString()
    # sk.toString()

    print("Message to encrypt: ", MSG)

    msg_enc = enc(MSG, pk)
    print("Encrypted message: ", msg_enc)

    msg_dec = dec(msg_enc, sk, pk)
    print("Message decrypted: ", msg_dec)


@main.command(help='Run the Secure Comparison Protocol')
def comp():

    num1, num2 = 4, 10
    # print("Comparing {} and {}".format(num1, num2))
    result = sqp(num1, num2)

    # print("Result: ", result)


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
