from src.constants.const import KEY_LEN, SEC_PARAM, DEB_AUX_TXT, DEB_AUX2_TXT
from src.functions.square_mult import square_mult
from src.paillier.paillier_key import *
from decimal import *
from src.functions.bcolors import bcolors

import random
import secrets


def calc_g(num):
    """
    Calculates "g"
    :param num: In this case it is n
    :return: g = n + 1
    """
    return num + 1  # Following the advice from the statement


def calc_l(x, n):
    """
    Calculates L(x)
    :param x:
    :param n:
    :return: L(x) result
    """
    return (x - 1) // n


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
    getcontext().prec = 10  # Set precision to use Decimal

    # Calculate 2^p_len to avoid recalculating it
    two_to_len = Decimal(2) ** Decimal(p_len)
    two_to_len_minus = Decimal(2) ** Decimal(p_len - 1)

    # The primes have to have half the size from the key
    lower_bound = two_to_len_minus + 1

    # Generate initial random number
    p_num = random.randint(lower_bound, two_to_len)

    # Check until a prime number is found
    while not is_prime(p_num, 128):
        # Calculate a new random number
        p_num = random.randint(int(lower_bound), two_to_len)

    return p_num  # Return obtained prime number


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
        while p == q or mu is None:  # To avoid to get the two prime numbers equal
            p = get_prime(KEY_LEN / 2)  # Each prime number has the half of the key's bit length
            q = get_prime(KEY_LEN / 2)
            mu = -1  # To avoid infinite loop

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
    # Get a random value from 0 to n
    rdn = secrets.randbelow(pk.n)

    # Calculate the exponential values
    g_m = square_mult(pk.g, msg, pk.n_2)
    r_n = square_mult(rdn, pk.n, pk.n_2)

    # Calculate the final value
    enc_msg = g_m * r_n % pk.n_2

    return enc_msg  # Return the message encrypted


def dec(enc_msg, sk, pk):
    """
    Decrypts a message "enc_msg" using the sk.
    The public key "pk" is used to get the modulus used for the operations
    :param enc_msg: Encrypted message
    :param sk: Secret Key
    :param pk: Public Key
    :return: The decrypted message
    """
    # Calculate the x value from L(x)
    x = square_mult(enc_msg, sk.lamb, pk.n_2)

    # Calculate3 L(x)
    l_result = calc_l(x, pk.n)

    # Calculate the final formula to get the decrypted message
    dec_msg = l_result * sk.mu % pk.n

    return dec_msg


def secure_addition(m1, m2, pk, n=None):
    """
    Performs a secure addition
    :param n: Modulus. Is only used when no pk is set
    :param m1: First encrypted message
    :param m2: Second encrypted message
    :param pk: Public Key
    :return: The addition performed
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
    :return: The scalar multiplication performed
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
    :return: The subtraction performed
    """
    if n is not None:  # No pk used, just modulus
        m2_aux = int(square_mult(m2, n - 1, n * n))
        return (m1 * m2_aux) % (n * n)

    else:  # PK used
        m2_aux = int(square_mult(m2, pk.n - 1, pk.n_2))
        return (m1 * m2_aux) % pk.n_2


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


def calc_z(num1, num2, pk, msg_len):
    """
    Calculates the value "z"
    :param num1: First encrypted number to be compared
    :param num2: Second encrypted number to be compared
    :param pk: Public Key
    :param msg_len: Length of the original plain text
    :return:
    """
    # Encrypt 2^l
    length_enc = enc(2 ** msg_len, pk)

    # add = [2^l] + [a]
    add = secure_addition(length_enc, num1, pk)

    # z = [2^l] + [a] - [b]
    z = secure_subst(add, num2, pk)

    return z


def calc_c(z, msg_len, sec_param, pk):
    """
    Calculates the value c
    :param z: Value z
    :param msg_len: Length of the original message
    :param sec_param: Security Parameter
    :param pk: Public Key
    :return: the value c and r
    """
    # Calculate the random value r
    r = sec_param + msg_len + 1

    # Encrypt r in order to be able to operate with it
    r_enc = enc(r, pk)

    # c = [z] + [r]
    c = secure_addition(z, r_enc, pk)

    return c, r  # Both c and r are returned


def calc_c_list(c, sk, pk, msg_len):
    """
    Calculates the encryption of all the bits of c
    :param c: Value c
    :param sk: Secret Key
    :param pk: Public Key
    :param msg_len: Length of the original message
    :return: A list with all the bits of c encrypted
    """
    dec_c = dec(c, sk, pk)  # Decrypt c

    dec_c = dec_c % (2 ** msg_len)  # Reduce c to mod 2^l

    dec_c_bin = num_to_bin(dec_c)  # To binary

    dec_c_bin = fill_left_zeros(dec_c_bin, msg_len - len(dec_c_bin))  # Check that no left zero is removed

    i = 0  # Initialize auxiliary variables
    c_list = []  # List for saving the encryptions of all the bits

    # Encrypt all the different bits and save them in a list
    while i < len(dec_c_bin):
        enc_i = enc(int(dec_c_bin[i]), pk)  # Encrypt the bit i
        c_list.append(enc_i)  # Add new element

        i += 1  # Update index

    # Reverse the order of the list to fit the logical model of the slides
    c_list = c_list[::-1]

    return c_list  # Return the encryption of all the bits


def calc_e_list(r, c_encrypt, pk, msg_len):
    """
    Calculates the list of e values
    :param r: Value r
    :param c_encrypt: List with the values from c encrypted
    :param pk: Public Key
    :param msg_len: Length of the original message
    :return:
    """
    # List which will store the values for e_i
    e_list = []

    # Calculate r modulus 2^l
    r_mod = r % 2 ** msg_len

    # Set r in modulus 2^l to binary
    r_bin = num_to_bin(r_mod)

    # Check that r has all the bit digits
    r_filled = fill_left_zeros(r_bin, msg_len - len(str(r_bin)))

    # r_filled as a list
    r_list = [int(x) for x in str(r_filled)]

    # Reverse the list of r in order to match the logical model of the slides
    r_list = r_list[::-1]

    for i, val in enumerate(c_encrypt):
        # Encode 1 to operate with it
        enc_1 = enc(1, pk)

        # Calculate [r_i]
        enc_r_i = enc(r_list[i], pk)

        # Perform the operations for the left addition
        # left_add_1 = [1] + [c_i]
        left_add_1 = secure_addition(enc_1, c_encrypt[i], pk)

        # left_add = [1] + [c_i] - [r_i]
        left_add = secure_subst(left_add_1, enc_r_i, pk)

        # Reset to zero the cumulative sum
        sum_op = enc(0, pk)

        # Calculate the sum
        for j in range(i + 1, msg_len):
            # enc_r_j = [r_j]
            enc_r_j = enc(r_list[j], pk)

            # left_sum_j = [c_j] + [r_j]
            left_sum_j = secure_addition(c_encrypt[j], enc_r_j, pk)

            # subs = [c_j] * [r_i]
            subs = secure_scalar_mult(c_encrypt[j], enc_r_j, pk)

            # left_sum_j = [c_j] + [r_j] - [c_j] * [r_i] - [c_j] * [r_i]
            left_sum_j = secure_subst(left_sum_j, subs, pk)
            left_sum_j = secure_subst(left_sum_j, subs, pk)

            # Update the sum value
            sum_op = secure_addition(sum_op, left_sum_j, pk)

        # e_i = left_add + sum_op
        e_i = secure_addition(left_add, sum_op, pk)

        # Add the calculated value to the list
        e_list.append(e_i)

    return e_list  # Return a list with all the e values


def check_e(e_list, pk, sk):
    # Go through all the e_i to check if there is a e_i = 0
    for i, val in enumerate(e_list):
        e_i = dec(e_list[i], sk, pk)
        # e_i = e_i % (2 ** msg_len)  # Reduce e_i to mod 2^l

        if e_i == 0:  # r larger than c
            return 1

    return 0  # c larger than r


def calc_final_z(c, r, msg_len, comp_result, sk, pk):
    # Encrypt the value r to operate with it
    enc_r = enc(r, pk)

    # subs = [c] - [r]
    subs = secure_subst(c, enc_r, pk)

    # right_add =  lambda{0,1} * 2^l
    right_add = comp_result * 2 ** msg_len
    # subs = secure_addition(subs, right_add, pk)

    # Get the most significant bit of z
    z = dec(subs, sk, pk) >> msg_len

    return z


def sqp(num1, num2, pk, sk, msg_len):
    """
    Performs the Secure Comparison Protocol
    :param msg_len: Length of the original message
    :param num1: First encrypted number to be compared
    :param num2: Second encrypted number to be compared
    :param sk: Secret Key
    :param pk: Public Key
    :return:
    """
    # Calculate z
    z = calc_z(num1, num2, pk, msg_len)

    c, r = calc_c(z, msg_len, SEC_PARAM, pk)

    c_encrypt = calc_c_list(c, sk, pk, msg_len)

    e_list = calc_e_list(r, c_encrypt, pk, msg_len)

    comp_result = check_e(e_list, pk, sk)

    result_cpm = calc_final_z(c, r, msg_len, comp_result, sk, pk)

    return result_cpm
