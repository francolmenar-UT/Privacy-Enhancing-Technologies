from constants.constants import keys_path
from functions.packet_prepare import create_message
from functions.network import connect, disconnect, send_message

while True:
    host = input("Host: ")
    port = int(input("Port: "))

    try:
        s = connect(host, port)
    except Exception as e:
        print("Unable to connect\n")
        print(e)
    else:
        break

while True:
    # Get a valid receiver and message
    while True:
        receiver = input("Receiver: ")
        msg = input("Message: ")

        if receiver and msg:
            break
        else:
            print("Receiver or Message not valid\n")

    message = create_message(receiver, msg, keys_path[::-1])

    try:
        response = send_message(message, s)
    except ValueError as e:
        print("Error in sending the message:")
        print(e)
    else:
        print("Message sent correctly!\n")

    stop = input("Insert stop to exit (nothing to continue): ")
    if stop == "stop":
        break

disconnect(s)
