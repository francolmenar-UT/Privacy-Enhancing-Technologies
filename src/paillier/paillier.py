from src.constants.const import KEY_LEN
from src.functions.square_mult import square_mult
from src.paillier.paillier_key import *

import random

import secrets


def calc_g(num):
    """
    Calculates "g"
    :param num: In this case it is n
    :return: g = n + 1
    """
    return num + 1  # Following advice from the statement


def calc_l(x, n):
    """
    Calculates L(x)
    :param x:
    :param n:
    :return: L(x) result
    """
    return (x - 1) / n


def calc_lambda(p_1, p_2):
    """
    As two prime numbers are coprime to each other,
    Lambda is going to be calculated using the euler totient
    :param p_1: First prime number
    :param p_2: Second prime number
    :return: Lambda
    """
    return (p_1 - 1) * (p_2 - 1)


def calc_mu(lamb, n):
    """
    Calculates mu by obtaining the multiplicative inverse of lambda, which is phi of
    :param n:
    :param lamb:
    :return: The result of mu
    """
    return mult_inv(lamb, n)


def e_gcd(a, b):
    """
    Extended euclidean implementation to calculate the gcd
    :param a:
    :param b:
    :return:n gcd of "a" and "b"
    """
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = e_gcd(b % a, a)
        return g, x - (b // a) * y, y


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


def mult_inv(num, n):
    """
    Calculates the multiplicative inverse of num in mod "n"
    :param num: Number to calculate the multiplicative inverse
    :param n: Modulus
    :return: The multiplicative inverse of num mod n
    """
    g, x, y = e_gcd(num, n)
    if g != 1:
        return None  # No multiplicative inverse exists
    else:
        return x % n  # Multiplicative inverse obtained


def key_gen():
    """
    Creates the keys for the Paillier Cryptosystem
    :return: The public and private keys obtained
    """
    n, lamb, p, q, mu = 0, 0, 0, 0, None  # Initialize values for using the while loop

    while mu is None:  # To ensure that mu have a correct value
        while p == q:  # To avoid to get the two prime numbers equal
            p = get_prime(KEY_LEN / 2)  # Each prime number has the half of the key's bit length
            q = get_prime(KEY_LEN / 2)

        lamb = calc_lambda(p, q)  # Calculate lambda

        n = p * q  # Calculate n

        g = calc_g(n)  # Calculate g

        mu = calc_mu(lamb, n)  # Calculate mu

    return PublicKey(n, g), PrivateKey(lamb, mu)


def enc(msg, pk):
    """
    Encrypts a message "msg" with the public key "pk"
    :param msg: Message to be encrypted
    :param pk: Public key to be used in the encryption
    :return: The encrypted value
    """
    rdn = secrets.randbelow(pk.n)  # Get a random value from 0 to n

    g_m = square_mult(pk.g, msg, pk.n_2)  # Calculate exponential values
    r_n = square_mult(rdn, pk.n, pk.n_2)
    return (g_m * r_n) % pk.n_2


def dec(enc_msg, sk, pk):
    """

    :param enc_msg:
    :param sk:
    :param pk:
    :return:
    """
    x = square_mult(enc_msg, sk.lamb, pk.n_2)
    return int(calc_l(x, pk.n) * sk.mu % pk.n)
