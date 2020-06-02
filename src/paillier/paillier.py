from src.constants.const import KEY_LEN
from src.paillier.paillier_key import *


def get_prime(len):
    """
    Creates a random prime number with at least the length "len"
    :param len: The minimum length of the prime numbers in bits
    :return: The random prime number
    """
    return 0


def calc_lambda(p_1, p_2):
    """
    Calculates lambda using the two input prime numbers
    :param p_1:
    :param p_2:
    :return: Lambda
    """
    # TODO calculate it using phi of n
    return 0


def calc_g(num):
    """
    Calculates "g"
    :param num:
    :return:
    """
    return num + 1  # Following advice from the statement


def calc_l(x, n):
    """
    Calculates L(x)
    :param x:
    :param n:
    :return:
    """
    return (x - 1) / n  # TODO Check if it is in mod n or n^2


def calc_mu(g, lamb, n_2, n):
    """
    Calculates mu
    :param g:
    :param lamb:
    :param n_2:
    :param n:
    :return:
    """
    x = g ** lamb % n_2  # Calculate the inside from the L()
    l_result = calc_l(x, n)

    # TODO calculate mu as inverse of phi of n
    return 0


def paillier():
    """
    Manages the calls to the different methods to run the Paillier Cryptosystem
    :return:
    """


def key_gen():
    """
    Creates the keys for the Paillier Cryptosystem
    :return: The public and private keys obtained
    """
    p, q = 0, 0  # Initialize values for using the while loop
    while p == q:  # To avoid to get the two prime numbers equal
        p = get_prime(KEY_LEN / 2)
        q = get_prime(KEY_LEN / 2)

    lamb = calc_lambda(p, q)  # Calculate lambda

    n = p * q  # Calculate n
    n_2 = n * n  # Calculate n^2

    g = calc_g(n_2)  # Calculate g

    mu = calc_mu(g, lamb, n_2, n)

    return PublicKey(n, g), PrivateKey(lamb, mu)
