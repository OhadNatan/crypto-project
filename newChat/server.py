import socket
import threading

# Global Vars
HOST = '10.0.0.25'
PORT = 9090
buffer_size = 1024
clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()


def broadcast(message):
    """
    Broadcast to all the clients the message args

    Parameters
    ----------
    message : bytes
        The message to broadcast to all clients
    """
    for client in clients:
        client.send(message)


def handle(client):
    """
    Handle the client messaging to the chat

    Parameters
    ----------
    client : socket
        The client object to handle
    """
    while True:
        index = clients.index(client)
        try:
            message = client.recv(buffer_size)
            print("{nickname}".format(nickname=nicknames[index]))
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    """
    Start the chat! The server starting to receiving client to handle with.
    Saving the socket and the nickname of the clients and staring new thread with handle func on each client
    """
    while True:
        client, address = server.accept()
        print("Connected with {add}!".format(add=str(address)))

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(buffer_size).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        nick = str(nickname)
        message_to_print = "The client's nickname is {nick}".format(nick=nick)
        print(message_to_print)
        message_to_broadcast = "{nick} connected to the server\n".format(nick=nick)
        broadcast(message_to_broadcast.encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is running")
receive()

