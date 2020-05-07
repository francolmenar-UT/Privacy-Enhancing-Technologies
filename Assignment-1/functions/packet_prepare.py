import sys
import struct
import binascii


def add_recipient(name, msg):
    """
    Adds the name of the receiver to the message to be sent

    TODO probably it can be removed and added to the main once everything works

    :param name: Receiver name
    :param msg: Message to be sent
    :return: The String with name added at the beginning of the message, separated by a coma
    """
    return name + "," + msg


def add_length(msg):
    """
     Append a 4 Byte length field indicating the number of bytes of msg
     The result is encoded into Big Endian unsigned integer

    :param msg: The original message to be sent
    :return: The original message msg with the 4 Byte length field as a suffix.
    """
    # size = sys.getsizeof(msg) # This gets the size of the whole variable, not just the string

    size = len(msg.encode('utf-8'))  # Get the size in bytes of the message

    new_size = struct.pack('>I', size)  # > is for big endian, I for unsigned int

    print("Size in bytes: " + str(size))

    print(binascii.hexlify(new_size))

    return str(new_size) + msg  # Add the size to the original message
