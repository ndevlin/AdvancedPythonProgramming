
"""
CaesarCypher Client
May 24 2024
"""

import socket
import unittest
import time
from ByteStreams_May15_NDevlin import ByteStream
from RotatorForCommand_May24 import Rotor
from Command_May24 import Command


class CypherClient:
    def __init__(self, stringToEncrypt="HELLO WORLD", initialPosition="$"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.stringToEncrypt = stringToEncrypt
        self.initialPosition = initialPosition

        self.incrementAmount = 1
        self.encrypted = ""
        self.decrypted = ""
        self.command = Command()

        self.asciiBegin = 0x20
        self.asciiEnd = 0x80

        self.connect()

        self.encryptAndDecrypt()


    def caesarCypher(self):
        self.encrypted = ""
        for char in self.stringToEncrypt:
            self.encrypted += self.rotate(char)
        return self.encrypted

    def rotate(self, char):
        self.command._set("increment")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes((message.bit_length() + 7) // 8, 'big')
        self.sendMessage(binaryMessage, binary=True)
        asciiVal = ord(char)
        self.command._set("getPosition")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes((message.bit_length() + 7) // 8, 'big')
        receivedMessage = self.sendMessage(binaryMessage, binary=True)
        position = int(receivedMessage)
        offset = position - self.asciiBegin
        newAsciiVal = asciiVal + offset

        self.command._set("rotationCounter")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes((message.bit_length() + 7) // 8, 'big')
        self.sendMessage(binaryMessage, binary=True)
        newAsciiVal = (newAsciiVal % self.asciiEnd) + self.asciiBegin
        
        return chr(newAsciiVal)
    
    def reverseRotate(self, char):
        self.command._set("increment")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        self.sendMessage(binaryMessage, binary=True)
        asciiVal = ord(char)

        self.command._set("getPosition")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        receivedMessage = self.sendMessage(binaryMessage, binary=True)
        position = int(receivedMessage)
        offset = position - self.asciiBegin

        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1

            self.command._set("rotationCounter")
            print(self.command)
            message = self.command._get()
            binaryMessage = message.to_bytes(1, 'big')
            self.sendMessage(binaryMessage, binary=True)

        return chr(newAsciiVal)


    def decryptCaesarCypher(self):
        self.decrypted = ""

        self.command._set("reset")
        print(self.command)
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        if message == 0: binaryMessage = b'\x00'
        self.sendMessage(binaryMessage)
        for char in self.encrypted:
            self.decrypted += self.reverseRotate(char)
        return self.decrypted


    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True
        print("Connected to server...")


    def sendMessage(self, message, binary=True):
        bytestream = ByteStream(message, isBinary=binary)
        self.sock.sendall(bytestream.get_bytes())
        response = self.sock.recv(1024)
        bytestream = ByteStream(response, isBinary=True)
        return bytestream.get_string()
    

    def encryptAndDecrypt(self):

        print("Encrypt", self.stringToEncrypt)
        self.caesarCypher()
        print("Encrypted:", self.encrypted)

        self.decryptCaesarCypher()
        print("Decrypted:", self.decrypted)

        try:
            query = ''
            while True:
                query = input("Client: ")
                if query.lower() == 'exit':
                    self.exit()
                    break
                else:
                    result = self.sendMessage(query)
                    if result.lower() == "exit":
                        print("Server exited")
                        print("Closing Connection")
                        self.sock.close()
                        break
                    print("Server:", result)
        except:
            print("Closing Connection")
            self.sock.close()
    

    def sendTextFile(self, filename):
        print("Attempting to send text file ", filename)
        try:
            self.connect()
            print("Connected to server...")
            lines = []
            with open(filename, 'r') as file:
                lines = file.readlines()
                print("Beginning to send file")
                for line in lines: 
                    bytestream = ByteStream(line)
                    self.sock.sendall(bytestream.get_bytes())
                    time.sleep(1)
            print("File sent, closing connection")
            bytestream = ByteStream("File sent, Client closing connection")
            self.sock.sendall(bytestream.get_bytes())
            time.sleep(1)
            bytestream = ByteStream("exit")
            self.sock.sendall(bytestream.get_bytes())
            self.sock.close()
        except:
            print("Error. Closing Connection")
            self.sock.close()
    
    def exit(self):
        print("Exiting")
        self.sendMessage("exit")
        print("Closing Connection")
        self.sock.close()


# Main

stringToEncrypt = "HELLO WORLDxyz+_)(*&^%$#@!{}~!"

client = CypherClient(stringToEncrypt)
client.encryptAndDecrypt()
