import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as padding_asymetric
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from constants.constants import IV_SIZE, KEY_SIZE


def encrypt_msg(msg, public_key_str):
    # Encrypt the message with aes
    ciphertext, aes_key, IV = aes_encrypt(msg)

    # Concatenate IV and aes_key
    aes_secret = IV + aes_key

    # Encrypt the aes_key and IV using RSA
    rsa_output = rsa_encrypt(aes_secret, public_key_str)

    # Concatenate the RSA encryption and the ciphertext
    return rsa_output + ciphertext


def rsa_encrypt(msg, public_key_str):
    # Create the pub key object from the string
    public_key = serialization.load_pem_public_key(
        public_key_str,
        backend=default_backend())

    # Encrypt the message
    ciphertext = public_key.encrypt(
        msg,
        padding_asymetric.OAEP(
            mgf=padding_asymetric.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    return ciphertext


def aes_encrypt(msg):
    key = os.urandom(KEY_SIZE)
    IV = os.urandom(IV_SIZE)

    padder = padding.PKCS7(128).padder()  # PKCS#7 padding
    padded_data = padder.update(msg)
    padded_data += padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, key, IV
