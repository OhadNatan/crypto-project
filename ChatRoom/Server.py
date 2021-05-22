import socket
import argparse
import os

one_fork = 0

# Create the parser
parser = argparse.ArgumentParser(description='create sever by IP and PORT given')

# Add the arguments
parser.add_argument('-IP',
                       type=str,
                       help='the host IP',
                       default="0.0.0.0")

parser.add_argument('-PORT',
                       type=int,
                       help='the server PORT',
                       default=2001)

# Execute the parse_args() method
args = parser.parse_args()

localIP = args.IP

localPort = args.PORT

bufferSize = 1024

msgFromServer = "Hello UDP Client"

bytesToSend = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    if one_fork == 0:
        one_fork = 1
        pid = os.fork()
        if pid:
            while True:
                # Sending a reply to client
                msgFromServer = input("Enter MSG:\n")
                bytesToSend = str.encode(str(msgFromServer))
                UDPServerSocket.sendto(bytesToSend, address)
