import socket
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='create sever by IP and PORT given')

# Add the arguments
parser.add_argument('-IP',
                       type=str,
                       help='the host IP',
                       default="10.0.0.23")

parser.add_argument('-PORT',
                       type=int,
                       help='the server PORT',
                       default=2001)

# Execute the parse_args() method
args = parser.parse_args()

localIP = args.IP

localPort = args.PORT

serverAddressPort = (localIP, localPort)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
while True:
    # Send to server using created UDP socket
    msgFromClient = input("Enter MSG:\n")
    if msgFromClient == "EXIT":
        bytesToSend = str.encode("I'm out, BYE!")
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        UDPClientSocket.close()
        break
    bytesToSend = str.encode(str(msgFromClient))
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)