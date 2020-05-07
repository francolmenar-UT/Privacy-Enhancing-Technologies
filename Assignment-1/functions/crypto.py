import pem


def encrypt_msg(msg, path_key):
    # TODO Create a random IV and key
    iv = "Random"
    key = "Random2"

    pk = pem.parse_file(path_key)  # Read the public key

    rsa_output = rsa_encrypt(iv, key, pk)  # Encrypt RSA

    aes_output = aes_encrypt(iv, key, msg)  # Encrypt AES

    return rsa_output + aes_output


def rsa_encrypt(iv, key, pk):
    concat = iv + key
    # TODO Encrypt concat with pk
    return "Result RSA"


def pkcs_7():
    return 0


def aes_encrypt(iv, key, msg):
    # TODO Add padding to the msg
    # TODO Encrypt with key and iv
    return "Result AES"


def oaep():
    return 0
