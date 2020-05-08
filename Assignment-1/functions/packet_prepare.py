import sys
import struct
import binascii
from functions.crypto import encrypt_msg


def create_message(recipient, message, mixers_keys):
    msg = add_recipient(recipient, message)

    # Create array of keys
    pub_keys = list()
    for path in mixers_keys:
        key_file = open(path, "rb")
        pub_keys.append(key_file.read())
        key_file.close()

    encrypted_message = encrypt_for_mixers(msg, pub_keys)

    final_message = add_length(encrypted_message)

    return final_message


def encrypt_for_mixers(msg, mixers_keys):
    for public_key in mixers_keys:
        msg = encrypt_msg(msg, public_key)

    return msg


def add_recipient(name, msg):
    """
    Adds the name of the receiver to the message to be sent, encoding the String
    in utf-8

    :param name: Receiver name
    :param msg: Message to be sent
    :return: The bytes representing the string <name>,<message>
    """

    return bytes(name + "," + msg, 'utf-8')


def add_length(msg):
    """
     Append a 4 Byte length field indicating the number of bytes of msg
     The result is encoded into Big Endian unsigned integer

    :param msg: The original message to be sent
    :return: The original message msg with the 4 Byte length field as a prefix.
    """

    size = struct.pack('>I', len(msg))  # > for big endian, I for unsigned int

    return size + msg  # Add the size to the original message
