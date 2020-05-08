from constants.constants import keys_path, HOST, PORT
from functions.packet_prepare import create_message
from functions.network import connect, disconnect, send_message

receiver = "Andrea"
msg = "Hey"

# The keys path must be in the order of encryption, so reverse the array
message = create_message(receiver, msg, keys_path[::-1])

print(message)

s = connect(HOST, PORT)

try:
    response = send_message(message, s)
except ValueError as e:
    print("Error in sending the message:")
    print(e)
else:
    print("Message sent correctly!")

disconnect(s)
