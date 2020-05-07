import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as padding_asymetric
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from constants.constants import iv_size, key_size


def encrypt_msg(msg, path_key):
    # TODO Fix sizes of the iv and key size
    iv = os.urandom(iv_size)  # Used for RSA
    key = os.urandom(key_size)

    with open(path_key, "rb") as key_file:  # Read the public key
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend())

    rsa_output = rsa_encrypt(iv, key, public_key)  # Encrypt RSA

    aes_output = aes_encrypt(msg)  # Encrypt AES

    return rsa_output + aes_output


def rsa_encrypt(iv, key, public_key):
    msg = iv + key  # The concatenation of the iv and the key is what is encrypted

    # TODO Take a look to the padding, it is not used the PKCS1-OAEP
    # TODO Check that the hashes are the correct ones

    ciphertext = public_key.encrypt(msg,
                                    padding_asymetric.OAEP(
                                        mgf=padding_asymetric.MGF1(algorithm=hashes.SHA1()),  # Changed to SHA-1
                                        algorithm=hashes.SHA1(),
                                        label=None)
                                    )

    return ciphertext


def aes_encrypt(msg):
    # TODO Check that it works

    key = os.urandom(128)  # Create the key
    iv = os.urandom(128)

    padder = padding.PKCS7(128).padder()  # PKCS#7 padding
    padded_data = padder.update(msg)
    padded_data += padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)  # Encrypt
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext
