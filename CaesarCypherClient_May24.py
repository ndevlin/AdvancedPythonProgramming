
"""
CaesarCypher Client
May 24 2024
"""

import socket
import json
import unittest
import time
from ByteStreams_May15_NDevlin import ByteStream
from RotatorForCommand_May24 import Rotor
from Command_May24 import Command

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True

    def sendMessage(self, message):
        bytestream = ByteStream(message)
        self.sock.sendall(bytestream.get_bytes())
        response = self.sock.recv(1024)
        bytestream = ByteStream(response, isBinary=True)
        return bytestream.get_string()
    
    def startTransmission(self):
        self.connect()
        print("Connected to server...")
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


class Decryption:
    def __init__(self, text=" ", initialPosition=" ", incrementAmount=1):
        self.text = text
        self.encrypted = ""
        self.decrypted = ""
        self.rotor = Rotor(initialPosition, incrementAmount)
        self.caesarCypher()

    def caesarCypher(self):
        self.encrypted = ""
        for char in self.text:
            self.encrypted += self.rotate(char)
        return self.encrypted

    def rotate(self, char):
        self.rotor.increment()
        asciiVal = ord(char)
        offset = self.rotor.position - self.rotor.asciiBegin
        newAsciiVal = asciiVal + offset

        aboveEndAmount = newAsciiVal // self.rotor.asciiEnd
        self.rotor.rotationCounter += aboveEndAmount
        newAsciiVal = (newAsciiVal % self.rotor.asciiEnd) + (aboveEndAmount * self.rotor.asciiBegin) - aboveEndAmount
        
        return chr(newAsciiVal)
    
    def reverseRotate(self, char):
        self.rotor.increment()
        asciiVal = ord(char)
        offset = self.rotor.position - self.rotor.asciiBegin

        newAsciiVal = asciiVal - offset
        if newAsciiVal < self.rotor.asciiBegin:
            newAsciiVal = self.rotor.asciiEnd - (self.rotor.asciiBegin - newAsciiVal) + 1
            self.rotor.rotationCounter += 1

        return chr(newAsciiVal)


    def decryptCaesarCypher(self):
        self.decrypted = ""
        self.rotor.reset()
        for char in self.encrypted:
            self.decrypted += self.reverseRotate(char)
        return self.decrypted


# Main


stringToEncrypt = "HELLO WORLDxyz+_)(*&^%$#@!{}~!"
print("Encrypt", stringToEncrypt)

decryption = Decryption(stringToEncrypt, "$")
print("Encrypted:", decryption.encrypted)

print("Decrypted:", decryption.decryptCaesarCypher())

client = Client()
client.startTransmission()
