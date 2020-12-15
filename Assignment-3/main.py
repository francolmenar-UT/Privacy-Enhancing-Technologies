from timeit import timeit

import click
import os
from pyfiglet import Figlet
from src.constants.const import *
from src.graph.createGraph import create_graph
from src.paillier.paillier import *
from src.functions.bcolors import bcolors


def create_val_list(tim_l):
    """
    Creates a list of values with the lengths provided in the list tim_l
    The amount of pairs of values are defined in TIM_PAIRS
    :param tim_l: List of lengths
    :return: A list of list with pairs
    """
    val_list = []  # List of values to be used

    # Go through all the different lengths
    for l_i in tim_l:
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
    return val_list


def create_folder(folder):
    """
    Checks if a folder exists, if it does not it creates it
    :param folder: Folder to be created
    :return:
    """
    # Check if the folder does not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)  # Create folder


def save_time(file, data_list, length):
    output_f = open(file, "w+")  # Open the output file
    data_str = ""

    # Save time against length
    for data in data_list:
        data_str += str(length) + ',' + str(data) + '\n'  # Append the data in a csv form

    output_f.write(data_str)  # Write the processed line to the output text file
    output_f.close()


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
@click.option('--interactive', '-i', is_flag=True, help='Ask for the values to the user')
def comp(input_num_1=None, input_num_2=None, verbose=False, interactive=False):
    # Get the numbers to compare from the user
    if interactive:
        verbose = True  # Set verbose to true if the user is introducing the values

        # Get the inputs from the user
        try:
            input_num_1 = int(input("First number to compare: "))
            input_num_2 = int(int(input("Second number to compare: ")))

            # Negative numbers not supported - It is not stated in the statement that they have to be supported
            if input_num_1 < 0 or input_num_2 < 0:
                print("{}Wrong input format: Introduce positive numbers please{}".format(bcolors.RED, bcolors.END))

        # Wrong format for the inputs from the user
        except:
            print("{}Wrong input format{}".format(bcolors.RED, bcolors.END))
            return

    if verbose:  # Print only if verbose flag is added in the execution command
        f = Figlet(font='slant')  # Useless cool text
        print(f.renderText('SQP'))
        if interactive:
            print("\tComparing {} and {}\n".format(input_num_1, input_num_2))  # Intro info message
        else:
            print("\tComparing {} and {}\n".format(TEST_NUM1, TEST_NUM2))  # Intro info message

    # Check if the input to chose is the Test values or values passed as arguments
    if input_num_1 is not None and input_num_2 is not None:  # Argument values
        num1 = input_num_1
        num2 = input_num_2
    else:  # Test values
        num1 = TEST_NUM1
        num2 = TEST_NUM2

    # Key generation
    pk, sk = key_gen()

    # Encryption of the numbers to be compared
    num1_enc = enc(num1, pk)
    num2_enc = enc(num2, pk)

    # Maximum length of the input messages
    msg_len = max(len(str(num_to_bin(num1))), len(str(num_to_bin(num2))))

    # Call to the Secure Comparison Protocol method
    result_cpm = sqp(num1_enc, num2_enc, pk, sk, msg_len)

    if verbose:
        # Printing the result of the comparison
        print("{}{} Results from Secure Comparison Protocol {}{}\n".format(bcolors.BLUE, SQP_TXT_AUX, SQP_TXT_AUX,
                                                                           bcolors.END))
        if result_cpm == 1:  # First Number larger
            print("{}{} is larger or equal than {}{}".format(bcolors.LIGHT_BLUE, num1, num2, bcolors.END))

        elif result_cpm == 0:  # Second Number larger
            print("{}{} is larger or equal than {}{}".format(bcolors.LIGHT_BLUE, num2, num1, bcolors.END))

        else:  # Error
            print(f"{bcolors.ERR}Incorrect result from comparison: {result_cpm}{bcolors.END}")


@main.command(help='Runs the SQP and stores the time data into csv files')
@click.option('-l', required=False)
def timer(l=None):
    """
    Generates the Graphs
    """
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('Timer'))

    l_list = []  # List of lengths

    # Run all the different lengths
    if l is None:
        l_list = TIM_L  # Set the default list of lengths

    # Run just the selected lengths
    else:
        l_split = l.split(",")  # Split the input by comas
        try:
            for l_i in l_split:  # Check all the input lengths
                l_int = int(l_i)
                if l_int in l_list:  # Repeated length error
                    print(f"{bcolors.RED}Error: Repeated length{bcolors.END}")
                    return -1
                if l_int in TIM_L:  # Append the new length
                    l_list.append(l_int)
                else:  # Wrong length error
                    print(f"{bcolors.RED}Error: Wrong length{bcolors.END}")
                    return -1
        except:  # Wrong format
            print(f"{bcolors.RED}Error: Wrong format for the length{bcolors.END}")
            return -1

        # Sort the list
        l_list.sort()

    # Create the list of values
    val_list = create_val_list(l_list)

    # Get the path to the python file for checking the existence of folder
    file_path = os.path.dirname(os.path.realpath(__file__))
    data_folder = file_path + "/" + DATA_F

    # Create folders for storing the timing data
    for folder in CREATE_FOLDERS:
        create_folder(file_path + "/" + folder)

    # Key generation for the execution
    pk, sk = key_gen()

    # Run the executions and save the execution times
    for l_idx, l_i in enumerate(l_list):
        time_list = []  # List with execution times

        for val_idx, val in enumerate(val_list[l_idx]):
            # Encryption of the numbers to be compared
            num1_enc = enc(val[0], pk)
            num2_enc = enc(val[1], pk)

            # Maximum length of the input messages
            msg_len = max(len(str(num_to_bin(val[0]))), len(str(num_to_bin(val[1]))))

            exe_time = timeit(lambda: sqp(num1_enc, num2_enc, pk, sk, msg_len), number=EXE_REP)
            time_list.append(exe_time/EXE_REP)

        # Check which is the length of the next list of executions
        if l_i == 10:
            out_file = data_folder + TIM_10_F + TIM_10_CSV  # Save the correct output file for later use
        elif l_i == 20:
            out_file = data_folder + TIM_20_F + TIM_20_CSV
        elif l_i == 50:
            out_file = data_folder + TIM_50_F + TIM_50_CSV
        elif l_i == 100:
            out_file = data_folder + TIM_100_F + TIM_100_CSV
        else:  # Error length
            print(f"{bcolors.RED}Wrong length used{bcolors.END}")
            return

        save_time(out_file, time_list, l_i)
    return 0


@main.command(help='Generates the Graphs from the data')
def graph():
    """
    Generates the Graphs
    """
    f = Figlet(font='slant')  # Useless cool text
    print(f.renderText('Graphs'))
    create_graph()
    return 0


main()  # Runs the cli
