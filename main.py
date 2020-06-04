import timeit

import click
from pyfiglet import Figlet
from src.constants.const import *
from src.paillier.paillier import *
from src.functions.bcolors import bcolors


def test_int_comp():
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

        if msg_dec != TEST_MSG:  # Error found - Not the same decryption as expected
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("{}Wrong decrypt: {}{}".format(bcolors.RED, msg_dec, bcolors.END))
            return  # Finish tests

    print(f"{bcolors.GREEN}No error while creating the keys-enc-dec {TICK}{bcolors.END}")  # Tests passed


@main.command(help='Run the Secure Comparison Protocol')
@click.option('--verbose', '-v', is_flag=True, help='Set the verbose to true')
@click.option('--debug', '-d', is_flag=True, help='Set debug to true')
def comp(verbose=False, debug=False):
    if debug:  # If debug is set, verbose is also used
        verbose = True

    if verbose:  # Print only if verbose flag is added in the execution command
        f = Figlet(font='slant')  # Useless cool text
        print(f.renderText('SQP'))
        print("\tComparing {} and {}\n".format(TEST_NUM1, TEST_NUM2))  # Intro info message

    # Key generation
    pk, sk = key_gen()

    # Encryption of the numbers to be compared
    num1_enc = enc(TEST_NUM1, pk)
    num2_enc = enc(TEST_NUM2, pk)

    # Maximum length of the input messages
    msg_len = max(len(str(num_to_bin(TEST_NUM1))), len(str(num_to_bin(TEST_NUM2))))

    # Call to the Secure Comparison Protocol method
    result_cpm = sqp(num1_enc, num2_enc, pk, sk, msg_len, verbose, debug)

    # Printing the result of the comparison
    print("{}{} Results from Secure Comparison Protocol {}{}\n".format(bcolors.BLUE, SQP_TXT_AUX, SQP_TXT_AUX,
                                                                       bcolors.END))
    if result_cpm == 1:  # First Number larger
        print("{}{} is larger or equal than {}{}".format(bcolors.LIGHT_BLUE, TEST_NUM1, TEST_NUM2, bcolors.END))

    elif result_cpm == 0:  # Second Number larger
        print("{} is larger or equal than {}".format(TEST_NUM2, TEST_NUM1))

    else:  # Error
        print(f"{bcolors.ERR}Incorrect result from comparison: {result_cpm}{bcolors.END}")


@main.command(help='Runs the SQP and stores the time data into csv files')
@click.option('-l', required=False)
def run_timer(l=None):
    """
    Generates the Graphs
    """
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('Run Timer'))

    val_list = []  # List of values to be used

    # Run all the different lengths
    if l is None:
        # Go through all the different lengths
        for l_i in TIM_L:
            val_i = []  # List with the pairs of elements for the length i
            lower_bound = 2 ** (l_i - 1) + 1  # 2^(L_1 - 1) + 1
            upper_bound = 2 ** l_i  # 2^(L_1)

            # For each length, go through all the different values to be created
            # The values are organized in pairs of elements
            for r_i in range(0, int(TIM_PAIRS)):
                # Generate the pair of values
                num1 = random.randint(lower_bound, upper_bound)
                num2 = random.randint(lower_bound, upper_bound)

                val_i.append([num1, num2])  # Add the new pair of elements created

            val_list.append(val_i)  # Add the new list of pairs of values of length l_i

        print(val_list)

    # Run just the selected lengths
    else:
        l_split = l.split(",")
        l_list = []
        try:
            for l_i in l_split:
                l_int = int(l_i)
                if l_int in l_list:
                    print("Repeated length")
                    return -1
                if l_int in TIM_L:
                    l_list.append(l_int)
                else:
                    print("Wrong length")
                    return -1
        except:
            print("Wrong format for the length")
            return -1

        l_list.sort()
        # TODO CREATE A METHOD WITH THE ABOVE LOOP TO CALL IT AND GENERATING THE PAIRS OF VALUES
    return 0


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
