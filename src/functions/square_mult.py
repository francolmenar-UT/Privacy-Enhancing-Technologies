def square_mult(m, e, n):
    """
    Calculates the Square-and-Multiply Algorithm
    :param m: Base of the exponentiation
    :param e: Exponent
    :param n: Modulus
    :return: The result of the operation
    """
    m = m % n  # Calculate the modulus of the message at first
    d_bin = bin(e)  # Convert the exponent to bit string
    d_bin = d_bin[:0] + d_bin[0 + 2:]  # Remove first two characters to have the correct bit array

    result = 1

    for i in range(0, len(d_bin)):  # Travers the whole bit string
        result = (result * result) % n  # a <- a^2  mod n
        if d_bin[i:i + 1] == '1':  # If the bit is 1, the result is multiplied by the base
            result = (result * m) % n
    return result
