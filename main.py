import timeit

import bcolors as bcolors
import click
from pyfiglet import Figlet
from src.constants.const import *
from src.paillier.paillier import *


def test_comp():
    # TODO REMOVE
    # num1, num2 = 10, 5  # First larger
    num1, num2 = 5, 10

    print("Bin numbs:")
    print(num_to_bin(num1))
    print(num_to_bin(num2))
    print(num_to_bin(2 ** 4))
    print()

    magic_length = max(
        len(str(num_to_bin(num1))),
        len(str(num_to_bin(num2)))) + 1

    # magic_length = len(str(num_to_bin(2 ** 4)))

    aux = 2 ** 4 + num1 - num2
    print(aux)

    aux_bin = num_to_bin(aux)
    aux_bin = fill_left_zeros(aux_bin, magic_length - len(str(aux_bin)))
    print(aux_bin)
    print(aux_bin[0])
    print()

    print("Change")

    num1, num2 = 10, 5

    aux = 2 ** 4 + num1 - num2
    print(aux)

    aux_bin = num_to_bin(aux)
    print(aux_bin)
    print(aux_bin[0])

    return


@click.group()
def main():
    pass


@main.command(help='Run execution tests to check that the correct value is obtained in the tests')
def test_pail():
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('Paillier Test'))
    print("Executing...")

    # Run the Paillier encryption as many times as it is defined in TEST_RANGE
    for i in range(0, TEST_RANGE):
        pk, sk = key_gen()  # Create key
        msg_enc = enc(TEST_MSG, pk)  # Encrypt Test Message
        msg_dec = dec(msg_enc, sk, pk)  # Decrypt Test Message

        if msg_dec != 100:  # Error found - Not the same decryption as expected
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Wrong decrypt:", msg_dec)
            return  # Finish tests

    print(f"{bcolors.PASS}No error while creating the keys-enc-dec {TICK}{bcolors.END}")  # Tests passed


@main.command(help='Run the Secure Comparison Protocol')
def comp():
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('SQP'))

    pk, sk = key_gen()

    num1, num2 = 15000000, 700

    print("\tComparing {} and {}\n".format(num1, num2))

    num1_enc = enc(num1, pk)
    num2_enc = enc(num2, pk)

    magic_length = max(
        len(str(num_to_bin(num1))),
        len(str(num_to_bin(num2))))
    print(magic_length)

    result = sqp(num1_enc, num2_enc, pk, sk, magic_length)

    # print("Result: ", result)


@main.command(help='Generates the Graphs from the data')
def graph():
    """
    Generates the Graphs
    """
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('Graphs'))
    # create_graph()
    return 0


main()  # Runs the cli
