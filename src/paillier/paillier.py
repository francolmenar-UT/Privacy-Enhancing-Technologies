import secrets
import random

from src.constants.const import KEY_LEN
from src.paillier.paillier_key import *


def is_prime(n, t=128):
    """
    Check if a number is prime or not
    :param n: Number to be checked if it is prime or not
    :param t: Maximum amount of tries for checking
    :return: True if it is prime. Otherwise False is returned
    """
    # Base cases
    if n == 2 or n == 3:
        return True

    # Non prime numbers' base case and even numbers
    if n <= 1 or n % 2 == 0:
        return False

    # Get r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    # Test the amount of times defined by "t"
    for _ in range(t):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)

        if x != 1 and x != n - 1:
            j = 1

            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:  # Not prime
                    return False
                j += 1

            if x != n - 1:  # Not prime
                return False
    return True


def get_prime(p_len):
    """
    Creates a random prime number with p_len bits
    :param p_len: The length of the prime numbers in bits
    :return: The random prime number
    """
    num = secrets.randbits(int(p_len))  # Create random number up to len bits

    # Check until a prime number is found
    while not is_prime(num, 128):
        num = secrets.randbits(int(p_len))  # Create a new random number to check

    return num


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
        p = get_prime(KEY_LEN / 2)  # Each prime number has the half of the key's bit length
        q = get_prime(KEY_LEN / 2)

    return

    lamb = calc_lambda(p, q)  # Calculate lambda

    n = p * q  # Calculate n
    n_2 = n * n  # Calculate n^2

    g = calc_g(n_2)  # Calculate g

    mu = calc_mu(g, lamb, n_2, n)

    return PublicKey(n, g), PrivateKey(lamb, mu)


28212031250264615512807258983629151942686779488304078199744659275300780260154293094172563731691536539195470111496322448986787977142091247971205149887615662508391907474272645564313231250361592165968076169562099266804714392196215690972853400589323069092023667367828825774513166236834718215683866273373743426172
