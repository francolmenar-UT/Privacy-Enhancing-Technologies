from constants.constants import keys_path, HOST, PORT
from functions.packet_prepare import create_message
from functions.network import connect, disconnect, send_message

receiver = "Andrea"
msg = "Hey"

# The keys path must be in the order of encryption, so reverse the array
message = create_message(receiver, msg, keys_path[::-1])

print(message)

s = connect(HOST, PORT)

response = send_message(message, s)

print("Response: {}".format(response))

disconnect(s)
