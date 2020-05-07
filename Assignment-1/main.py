from constants.constants import path_key_3
from functions.crypto import encrypt_msg
from functions.packet_prepare import add_recipient, add_length

msg = add_recipient("Andrea", "Hi")  # Prepend the recipient to the message

print("Message with the recipient added: " + msg)

# -------- First Encryption Step  - Mixer 3 -------- #
# encrypt_msg(msg, path_key_3)

# -------- Second Encryption Step - Mixer 2 -------- #


# -------- Third Encryption Step  - Mixer 1 -------- #


msg = add_length(msg)  # Add the length of the message
print("Message with the length added: " + msg)
