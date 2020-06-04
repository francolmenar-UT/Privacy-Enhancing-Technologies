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

    for i in range(0, 500):
        pk, sk = key_gen()
        msg_enc = enc(MSG, pk)
        msg_dec = dec(msg_enc, sk, pk)

        if msg_dec != 100:
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Wrong decrypt:", msg_dec)
            print("Again")
            msg_enc = enc(MSG, pk)
            msg_dec = dec(msg_enc, sk, pk)
            print("Dec again: ", msg_dec)

            pk.toString()
            sk.toString()
            return

        print(msg_dec)


def test_comp():
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


@main.command(help='Run the Secure Comparison Protocol')
def comp():
    pk, sk = key_gen()

    num1, num2 = 10, 5

    print("\tComparing {} and {}\n".format(num1, num2))

    num1_enc = enc(num1, pk)
    num2_enc = enc(num2, pk)

    magic_length = max(
        len(str(num_to_bin(num1))),
        len(str(num_to_bin(num2)))) + 1

    print(magic_length)

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
