import socket
import sys

class Tcp_Client:
    def tcp_Protocol_clientSide():
        HOST = "127.0.0.1"
        PORT = 40252
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection to server
        s.connect((HOST, PORT))
        # recieve Username
        username = input("Enter a username: ")
        while True:
                # Recieve message
            msg = input("\nMessage: ").lower()
            if msg == "quit" or msg == "disconnect":
                print("User has left")
                # s.send(msg)
                s.close()
                sys.exit(0)
                break
            else:
                msgPrepend = f"<<{username}>> {msg}"
                send_msg = bytearray(msgPrepend, "UTF-8")
                # Send Msg to server
                s.send(send_msg)
                # Recieve Reply from server
                recieved = s.recv(2040)
                recv_msg = recieved.decode()
                print(recv_msg)

Tcp_Client.tcp_Protocol_clientSide()