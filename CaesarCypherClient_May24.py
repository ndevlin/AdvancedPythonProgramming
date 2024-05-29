
"""
CaesarCypher Client
May 24 2024
"""

import socket
import time
from ByteStreams_May15_NDevlin import ByteStream
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


    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True
        print("Connected to server...")

    def caesarCypher(self):
        self.encrypted = ""
        for char in self.stringToEncrypt:
            self.encrypted += self.rotate(char)
        return self.encrypted

    def rotate(self, char):
        self.command._set("increment")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        self.sendMessage(binaryMessage, binary=True)

        asciiVal = ord(char)
        self.command._set("getPosition")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        receivedMessage = self.sendMessage(binaryMessage, binary=True)
        position = int(receivedMessage)
        offset = position - self.asciiBegin
        newAsciiVal = asciiVal + offset

        self.command._set("rotationCounter")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        self.sendMessage(binaryMessage, binary=True)

        aboveEndAmount = newAsciiVal // self.asciiEnd
        newAsciiVal = (newAsciiVal % self.asciiEnd) + (aboveEndAmount * self.asciiBegin) - aboveEndAmount
        newChar = chr(newAsciiVal)
        
        return newChar
    
    def reverseRotate(self, char):
        self.command._set("increment")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        self.sendMessage(binaryMessage, binary=True)

        asciiVal = ord(char)
        self.command._set("getPosition")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        receivedMessage = self.sendMessage(binaryMessage, binary=True)
        position = int(receivedMessage)
        offset = position - self.asciiBegin
        newAsciiVal = asciiVal - offset

        if newAsciiVal < self.asciiBegin:
            newAsciiVal = self.asciiEnd - (self.asciiBegin - newAsciiVal) + 1

            self.command._set("rotationCounter")
            message = self.command._get()
            binaryMessage = message.to_bytes(1, 'big')
            self.sendMessage(binaryMessage, binary=True)
        newChar = chr(newAsciiVal)

        return newChar

    def decryptCaesarCypher(self):
        self.decrypted = ""

        self.command._set("reset")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        if message == 0: binaryMessage = b'\x00'    # 0 gets interpreted as no data otherwise
        self.sendMessage(binaryMessage)
        for char in self.encrypted:
            self.decrypted += self.reverseRotate(char)
        return self.decrypted


    def sendMessage(self, message, binary=True):
        bytestream = ByteStream(message, isBinary=binary)
        self.sock.sendall(bytestream.get_bytes())
        response = self.sock.recv(1024)
        bytestream = ByteStream(response, isBinary=True)
        return bytestream.get_string()
    

    def encryptAndDecrypt(self):
        try:
            print("Encrypt", self.stringToEncrypt)
            self.caesarCypher()
            print("Encrypted:", self.encrypted)

            self.decryptCaesarCypher()
            print("Decrypted:", self.decrypted)

            self.exit()

        except:
            print("Closing Connection")
            self.sock.close()

    def exit(self):
        print("Exiting")
        self.command._set("close")
        message = self.command._get()
        binaryMessage = message.to_bytes(1, 'big')
        self.sendMessage(binaryMessage, binary=True)
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


# Main
stringToEncrypt = "HELLO WORLDxyz+_)(*&^%$#@!{}~!"

client = CypherClient(stringToEncrypt)
client.encryptAndDecrypt()

