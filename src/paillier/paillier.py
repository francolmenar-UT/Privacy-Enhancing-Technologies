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
    return (x - 1) // n


def calc_lambda(p_1, p_2):
    """
    As two prime numbers are coprime to each other,
    Lambda is going to be calculated using the euler totient
    :param p_1: First prime number
    :param p_2: Second prime number
    :return: Lambda
    """
    #
    # print("p: ", p_1)
    # print("q: ", p_2)
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
    # print("Length: ", int(p_len))

    lower_bound = (2 ** (p_len - 1)) + 1

    num = random.randint(int(lower_bound), 2 ** p_len)
    # num = secrets.randbits(int(p_len))  # Create random number up to len bits
    # print(num)

    # Check until a prime number is found
    while not is_prime(num, 128):
        num = random.randint(int(lower_bound), 2 ** p_len)
        # num = secrets.randbits(int(p_len))  # Create a new random number to check

    # print("Prime: ", num)
    # print("Prime bin: ", bin(num))
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
    rdn = secrets.randbelow(pk.n)  # Get a random value from 0 to n
    # print("Random: ", rdn)

    g_m = square_mult(pk.g, msg, pk.n_2)  # Calculate exponential values
    # g_m = pk.g ** msg
    r_n = square_mult(rdn, pk.n, pk.n_2)
    # r_n = rdn ** pk.n

    # print("G_m: ", g_m)
    # print("R_n: ", r_n)
    # print("R_n: ", r_n)
    enc_msg = (g_m * r_n) % (pk.n * pk.n)
    # print("Encrypt: ", enc_msg)
    return enc_msg


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
    # print("Enc: ", enc_msg)
    # print("Lambda: ", sk.lamb)
    # x = enc_msg ** sk.lamb
    # print("x 1: ", x)
    x = x % pk.n_2
    # print("x 2: ", x)
    l_result = calc_l(x, pk.n)
    # print("L(x): ", l_result)
    dec_aux = l_result * sk.mu
    # print("L(x) * mu: ", dec_aux)
    dec_msg = dec_aux % pk.n
    # print("Dec msg in: ", dec_msg)
    # print("n: ", pk.n)
    return dec_msg  # Calculate the resulting value


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
    if n is not None:  # No pk used, just modulus
        m2_aux = int(square_mult(m2, n - 1, n * n))
        return (m1 * m2_aux) % (n * n)

    else:
        m2_aux = int(square_mult(m2, pk.n - 1, pk.n_2))
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


def calc_z(num1, num2, pk, magic_length, sk):
    """
    Calculates the value "z"
    :param num1: First encrypted number to be compared
    :param num2: Second encrypted number to be compared
    :param pk: Public Key
    :param magic_length: Length of the original plain text
    :return:
    """
    print("++++++++++++++++ calc_z ++++++++++++++++")
    print("Num1 enc: ", num1)
    print("Num1: ", dec(num1, sk, pk))
    print("Num2 enc: ", num2)
    print("Num2: ", dec(num2, sk, pk))
    print("Len: ", 2 ** magic_length)
    print()

    # First addition
    length_enc = enc(2 ** magic_length, pk)

    add = secure_addition(length_enc, num1, pk)
    print("Add of {} + {} = {}".format(
        dec(length_enc, sk, pk),
        dec(num1, sk, pk),
        dec(add, sk, pk)))

    z = secure_subst(add, num2, pk)

    print("Subs of {} - {} = {}".format(
        dec(add, sk, pk),
        dec(num2, sk, pk),
        dec(z, sk, pk)))
    print()

    print("Z: ", z)
    print("Decrypted Z: ", dec(z, sk, pk))
    print(num_to_bin(dec(z, sk, pk)))

    # Subtraction
    return z


def calc_c(z, magic_length, sec_param, pk, sk):
    """
    Calculates the value c
    :param z: Value z
    :param magic_length: Length of the original message
    :param sec_param: Security Parameter
    :param pk: Public Key
    :return:
    """
    print("\n++++++++++++++++ calc_c ++++++++++++++++")
    print("Z: ", dec(z, sk, pk))
    print("Magic_length: ", magic_length)
    print("sec_param: ", sec_param)
    print()

    r = sec_param + magic_length + 1
    r_enc = enc(r, pk)

    print("r: ", r)
    print("r enc: ", r_enc)
    print("r dec: ", dec(r_enc, sk, pk))
    print()

    c = secure_addition(r_enc, z, pk)

    print("Add of {} + {} =  {}".format(
        dec(r_enc, sk, pk),
        dec(z, sk, pk),
        dec(c, sk, pk)
    ))
    print()

    print("C: ", c)
    print("Decrypted C: ", dec(c, sk, pk))
    print("r: ", r)

    return c, r


def calc_c_list(c, sk, pk, magic_length):
    """
    Calculates the encryption of all the bits of c
    :param c: Value c
    :param sk: Secret Key
    :param pk: Public Key
    :param magic_length: Length of the original message
    :return: A list with all the bits of c encrypted
    """
    print("\n++++++++++++++++ calc_c_list ++++++++++++++++")
    print("C: ", dec(c, sk, pk))
    print("C bin: ", num_to_bin(dec(c, sk, pk)))
    print("Magic_length: ", magic_length)
    print()

    dec_c = dec(c, sk, pk)  # Decrypt c
    print("C before mod: ", dec_c)
    dec_c = dec_c % (2 ** magic_length)  # Reduce c to mod 2^l
    print("C after mod: ", dec_c)

    dec_c_bin = num_to_bin(dec_c)  # To binary

    print("C in bin: ", dec_c_bin)

    dec_c_bin = fill_left_zeros(dec_c_bin, magic_length - len(dec_c_bin))  # Check that no left zero is removed

    print("C in bin filled: ", dec_c_bin)
    print()

    i = 0  # Initialize auxiliary variables
    c_list = []  # List for saving the encryptions of all the bits

    # Encrypt all the different bits and save them in a list
    while i < len(dec_c_bin):
        enc_i = enc(int(dec_c_bin[i]), pk)  # Encrypt the bit i  # TODO HERE HAPPENS SOMETHING
        c_list.append(enc_i)  # Add new element

        i += 1  # Update index

    c_list = c_list[::-1]

    for i, val in enumerate(c_list):
        print("c_list[{}] = {}".format(i, dec(c_list[i], sk, pk)))

    return c_list  # Return the encryption of all the bits


def calc_e_list(r, c_encrypt, pk, magic_length, sk):
    """
    Calculates the list of e values
    :param r: Value r
    :param c_encrypt: List with the values from c encrypted
    :param pk: Public Key
    :param magic_length: Length of the original message
    :return:
    """
    print("\n++++++++++++++++ calc_e_list ++++++++++++++++")
    for i, val in enumerate(c_encrypt):
        print("c_list[{}] = {}".format(i, dec(c_encrypt[i], sk, pk)))
    print("r ", r)
    print("Magic_length: ", magic_length)
    print()

    e_list = []
    print("r before fill: ", r)

    r = r % 2 ** magic_length

    print("r after mod: ", r)

    r = num_to_bin(r)

    print("r in bin", r)

    r_filled = fill_left_zeros(r, magic_length - len(str(r)))  # Check that no left zero is removed
    print("r after fill: ", r_filled)

    r_list = [int(x) for x in str(r_filled)]
    r_list = r_list[::-1]
    print("r as list reverted:", r_list)

    for i, val in enumerate(c_encrypt):
        print("\n\t\t +++++++++++++++++++++++++ I: {}  +++++++++++++++++++++++++".format(i))
        # print("original c_encrypt[{}]: {}".format(i, c_encrypt[i]))
        print("Dec c_list[{}] = {}".format(i, dec(c_encrypt[i], sk, pk)))
        print()

        # Left addition
        enc_1 = enc(1, pk)  # Get the encryption of the elements

        enc_c_i = c_encrypt[i]

        enc_r_i = enc(r_list[i], pk)

        left_add = secure_addition(enc_1, enc_c_i, pk)  # Perform the operations for left addition

        print("enc_c_i dec: ", dec(enc_c_i, sk, pk))
        print("Result add: {}".format(dec(left_add, sk, pk)))
        print()

        print("r_list[{}] dec: {}".format(i, dec(enc_r_i, sk, pk)))
        left_add = secure_subst(left_add, enc_r_i, pk)
        print("Result subs: {}".format(dec(left_add, sk, pk)))

        sum_op = enc(0, pk)  # Cumulative sum for the loop

        print("\n\t------------------ J ------------------")
        print("Initial value for cumulative sum: ", dec(sum_op, sk, pk))
        for j in range(i + 1, magic_length):  # Sum operation
            print("\n\t-------- J: {} --------".format(j))
            enc_c_j = c_encrypt[j]

            # print("original c_encrypt[{}]: {}".format(i, c_encrypt[j]))
            print("Dec c_encrypt[{}] = {}".format(j, dec(enc_c_j, sk, pk)))

            enc_r_j = enc(r_list[j], pk)

            print()
            print("Dec r_list[{}] = {}".format(j, dec(enc_r_j, sk, pk)))
            print()

            left_sum_j = secure_addition(enc_c_j, enc_r_j, pk)  # Calculate the sum for iteration j

            print("Result add {} + {} =  {}".format(dec(enc_c_j, sk, pk),
                                                    dec(enc_r_j, sk, pk),
                                                    dec(left_sum_j, sk, pk)
                                                    ))

            subs = secure_scalar_mult(enc_c_j, r_list[j], pk)

            left_sum_j = secure_subst(left_sum_j, subs, pk)
            left_sum_j = secure_subst(left_sum_j, subs, pk)

            sum_op = secure_addition(sum_op, left_sum_j, pk)  # Add the calculated value to the cumulative sum

            print("Result add =  {}".format(dec(sum_op, sk, pk)
                                            ))
        print("Outside of the sum")
        e_i = secure_addition(left_add, sum_op, pk)  # Calculate final e_i value
        print("Result sum add {} + {} =  {}".format(dec(left_add, sk, pk),
                                                    dec(sum_op, sk, pk),
                                                    dec(e_i, sk, pk)
                                                    ))

        e_list.append(e_i)  # Add the calculated value to the list

    print()
    for i, val in enumerate(e_list):
        # print(e_list[i])
        print("e_list[{}] = {}".format(i, dec(e_list[i], sk, pk)))

    return e_list  # Return a list with all the e values


def check_e(e_list, pk, sk, magic_length):
    print("\n++++++++++++++++ check_e ++++++++++++++++")

    for i, val in enumerate(e_list):
        e_i = dec(e_list[i], sk, pk)
        # e_i = e_i % (2 ** magic_length)  # Reduce e_i to mod 2^l

        print("e_list[{}] = {}".format(i, dec(e_list[i], sk, pk)))
        if e_i == 0:  # r larger than c
            return 1
    return 0


def calc_final_z(c, r, magic_length, comp_result, sk, pk):
    print(dec(c, sk, pk))
    print(r)
    enc_r = enc(r, pk)
    z = secure_subst(c, enc_r, pk)
    right_add = comp_result * 2 ** magic_length

    # z = secure_addition(z, right_add, pk)

    print("Z dec: ", dec(z, sk, pk))
    print(len(str(num_to_bin(dec(z, sk, pk)))))

    print(magic_length)

    print("Final result: ", dec(z, sk, pk) >> magic_length)


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
    int_1, int_2, len_i = 5, 10, 4
    sust = 2 ** len_i + int_1

    z = calc_z(num1, num2, pk, magic_length, sk)

    c, r = calc_c(z, magic_length, SEC_PARAM, pk, sk)

    c_encrypt = calc_c_list(c, sk, pk, magic_length)

    e_list = calc_e_list(r, c_encrypt, pk, magic_length, sk)

    comp_result = check_e(e_list, pk, sk, magic_length)

    calc_final_z(c, r, magic_length, comp_result, sk, pk)

    return 0
