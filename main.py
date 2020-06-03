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
    print("Gen..")
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
    pk, sk = key_gen()

    num1, num2 = 5, 10
    print("\tComparing {} and {}\n".format(num1, num2))

    num1_enc = enc(num1, pk)
    num2_enc = enc(num2, pk)

    magic_length = 4

    result = sqp(num1_enc, num2_enc, pk, sk, magic_length)

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
