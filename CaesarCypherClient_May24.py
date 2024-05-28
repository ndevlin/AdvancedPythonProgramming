
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
        self.rotor = Rotor(initialPosition, self.incrementAmount)

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
        self.rotor.increment()
        asciiVal = ord(char)
        self.command._set("getPosition")
        print(self.command)
        offset = self.rotor.position - self.asciiBegin
        newAsciiVal = asciiVal + offset

        aboveEndAmount = newAsciiVal // self.asciiEnd

        self.command._set("rotationCounter")
        print(self.command)
        self.rotor.rotationCounter += aboveEndAmount
        newAsciiVal = (newAsciiVal % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount
        
        return chr(newAsciiVal)
    
    def reverseRotate(self, char):
        self.command._set("increment")
        print(self.command)
        self.rotor.increment()
        asciiVal = ord(char)

        self.command._set("getPosition")
        print(self.command)
        offset = self.rotor.position - self.asciiBegin

        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1

            self.command._set("rotationCounter")
            print(self.command)
            self.rotor.rotationCounter += 1

        return chr(newAsciiVal)


    def decryptCaesarCypher(self):
        self.decrypted = ""

        self.command._set("reset")
        print(self.command)
        self.rotor.reset()
        for char in self.encrypted:
            self.decrypted += self.reverseRotate(char)
        return self.decrypted


    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True
        print("Connected to server...")


    def sendMessage(self, message):
        bytestream = ByteStream(message)
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
