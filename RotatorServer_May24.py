
"""
Rotator Server
May 24 2024
"""

import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from RotatorForCommand_May24 import Rotor

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12346))

    def startInteractive(self):
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            userInput = ''
            while userInput.lower() != 'exit':
                data = conn.recv(1024)
                if data:
                    response = data.decode('utf-8')
                    print("Client:", response)
                    if response.lower() == 'exit':
                        print("Client exited")
                        break
                    userInput = input("Server: ")
                    bytestream = ByteStream(data=userInput, isBinary=False)
                    conn.sendall(bytestream.get_bytes())
            print("Exiting")
            print("Closing Connection")
            conn.close()
        except:
            print("Closing Connection")
            conn.close()
    

    def startReceiveTextFile(self):
        print("Attempting to Receive Text File")
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            print("Connected...")
            receivedData = ""
            while receivedData.lower() != 'exit':
                data = conn.recv(1024)
                if data:
                    receivedData = data.decode('utf-8')
                    print(receivedData)
                    if receivedData.lower() == 'exit':
                        print("Client exited")
                        break
            print("Closing Connection")
            conn.close()
        except:
            print("Error. Closing Connection")
            conn.close()

if __name__ == '__main__':
    server = Server()
    server.startInteractive()