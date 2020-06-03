from src.constants.const import KEY_LEN, SEC_PARAM
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
    n, lamb, g, p, q, mu = 0, 0, 0, 0, 0, None  # Initialize values for using the while loop

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
    Decrypts a message "enc_msg" using the sk.
    The public key "pk" is used to get the modulus used for the operations
    :param enc_msg: Encrypted message
    :param sk: Secret Key
    :param pk: Public Key
    :return:
    """
    x = square_mult(enc_msg, sk.lamb, pk.n_2)  # Calculate the value inside L(x)
    return int(calc_l(x, pk.n) * sk.mu % pk.n)  # Calculate the resulting value


def secure_addition(m1, m2, pk, n=None):
    """
    Performs a secure addition
    :param n: Modulus. Is only used when no pk is set
    :param m1: First encrypted message
    :param m2: Second encrypted message
    :param pk: Public Key
    :return:
    """
    if n is not None:  # No pk used, just modulus
        return (m1 * m2) % (n * n)

    return (m1 * m2) % pk.n_2  # pk used


def secure_scalar_mult(m1, c, pk, n=None):
    """
    Performs a secure scalar multiplication
    :param n: Modulus. Is only used when no pk is set
    :param m1: First encrypted message
    :param c: Scalar variable to be used in the multiplication
    :param pk: Public Key
    :return:
    """
    if n is not None:  # No pk used, just modulus
        return int(square_mult(m1, c, n * n))

    return int(square_mult(m1, c, pk.n_2))  # pk used


def secure_subst(m1, m2, pk, n=None):
    """
    Performs a Secure Subtraction
    :param n: Modulus. Is only used when no pk is set
    :param m1: First encrypted message
    :param m2: Second encrypted message
    :param pk: Public Key
    :return:
    """
    m2_aux = int(square_mult(m2, pk.n - 1, pk.n_2))

    if n is not None:  # No pk used, just modulus
        return (m1 * m2_aux) % (n * n)

    return (m1 * m2_aux) % pk.n_2  # pk used


def num_to_bin(num):
    """
    Covert a number into its bit string representation
    :param num: Number to be converted to Bit String
    :return: The resulting Bit String
    """
    b_num = bin(num)  # Num to bit string
    return b_num[:0] + b_num[0 + 2:]  # Remove first two characters to have the correct bit array


def fill_left_zeros(b_num, amount):
    """
    Fill with zeros at the left of the Bit String
    :param b_num: Bit String to be used
    :param amount: Number of zeros to be added
    :return: The new Bit String with the zeros added to the left
    """
    return "0" * amount + str(b_num)  # Append the zeros to the left


def set_b_len(b_num1, b_num2):
    """
    Equal the size of two bit strings by adding zeros to the left
    :param b_num1: First Bit String
    :param b_num2: Second String
    :return: The new Bit Streams with the same length
    """
    # Obtain the length of the bit strings
    b_len1, b_len2 = len(b_num1), len(b_num2)

    # First bit string larger
    if b_len1 > b_len2:
        b_len_max = b_len1
        b_num2 = fill_left_zeros(b_num2, b_len_max - len(b_num2))

    # Second bit string larger
    elif b_len2 > b_len1:
        b_len_max = b_len2
        b_num1 = fill_left_zeros(b_num1, b_len_max - len(b_num1))

    return str(b_num1), str(b_num2), len(b_num1)


def calc_z(num1, num2, pk, magic_length):
    """
    Calculates the value "z"
    :param num1: First encrypted number to be compared
    :param num2: Second encrypted number to be compared
    :param pk: Public Key
    :param magic_length: Length of the original plain text
    :return:
    """
    # First addition
    length_enc = enc(2 ** magic_length, pk)
    add = secure_addition(length_enc, num1, pk)

    # Subtraction
    return secure_subst(add, num2, pk)


def calc_c(z, magic_length, sec_param, pk):
    """
    Calculates the value c
    :param z: Value z
    :param magic_length: Length of the original message
    :param sec_param: Security Parameter
    :param pk: Public Key
    :return:
    """
    r = sec_param + magic_length + 1
    r_enc = enc(r, pk)

    return secure_addition(r_enc, z, pk)


def encrypt_c(c, sk, pk, magic_length):
    """
    Calculates the encryption of all the bits of c
    :param c: Value c
    :param sk: Secret Key
    :param pk: Public Key
    :param magic_length: Length of the original message
    :return: A list with all the bits of c encrypted
    """
    dec_c = dec(c, sk, pk)  # Decrypt c
    dec_c = dec_c % (2 ** magic_length)  # Reduce c to mod 2^l

    dec_c_bin = num_to_bin(dec_c)  # To binary

    i = 0  # Initialize auxiliary variables
    c_list = []  # List for saving the encryptions of all the bits

    # Encrypt all the different bits and save them in a list
    while i < len(dec_c_bin):
        enc_i = enc(int(dec_c_bin[i]), pk)  # Encrypt the bit i
        c_list.append(enc_i)  # Add new element

        i += 1  # Update index

    return c_list  # Return the encryption of all the bits


def sqp(num1, num2, pk, sk, magic_length):
    """
    Performs the Secure Comparison Protocol
    :param magic_length: Length of the original message
    :param num1: First encrypted number to be compared
    :param num2: Second encrypted number to be compared
    :param sk: Secret Key
    :param pk: Public Key
    :return:
    """

    z = calc_z(num1, num2, pk, magic_length)
    c = calc_c(z, magic_length, SEC_PARAM, pk)

    c_encrypt = encrypt_c(c, sk, pk, magic_length)
    print(c_encrypt)

    return 0
