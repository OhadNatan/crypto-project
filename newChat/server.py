import socket
import threading

HOST = '10.0.0.17'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):

    while True:
        index = clients.index(client)
        try:
            message = client.recv(1024)
            print("{nickname}".format(nickname=nicknames[index]))
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {add}!".format(add=str(address)))

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        message_to_print = "Nickname of the client is {nick}!".format(nick=str(nickname))
        print(message_to_print)
        message_to_broadcast = "{nick} connected to the server!\n".format(nick=str(nickname))
        broadcast(message_to_broadcast.encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server is running")
receive()

