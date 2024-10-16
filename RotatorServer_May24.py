
"""
Rotator Server
May 24 2024
"""

import socket
from ByteStreams_May15_NDevlin import ByteStream
from RotatorForCommand_May24 import Rotor

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12345))

        self.asciiBegin = 0x20
        self.asciiEnd = 0x80
        self.initialPosition = "$"
        self.incrementAmount = 1
        self.rotor = Rotor(self.initialPosition, self.incrementAmount, self.asciiBegin, self.asciiEnd)


    def startTransmission(self):
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            rotorResponse = ''
            while rotorResponse != 0b111:
                data = conn.recv(1)
                data = int.from_bytes(data, 'big')
                if data != None:
                    print("Client:", data)
                    if data == 0b111:
                        print("Client exited")
                        break
                    rotorResponse = self.rotorResponse(data)
                    if rotorResponse:
                        print("Sending Response: ", rotorResponse)
                        bytestream = ByteStream(data=rotorResponse, isBinary=False)
                        conn.sendall(bytestream.get_bytes())
                    else:
                        print("Sending Response: -1")
                        bytestream = ByteStream(data="-1", isBinary=False)
                        conn.sendall(bytestream.get_bytes())
            print("Exiting")
            print("Closing Connection")
            conn.close()
        except:
            print("Error: Closing Connection")
            conn.close()

    def rotorResponse(self, data):
        if data == 0b000:
            self.rotor.reset()
        elif data == 0b001:
            self.rotor.increment()
            return self.rotor.__str__()
        elif data == 0b010:
            self.rotor.decrement()
            return self.rotor.__str__()
        elif data == 0b011:
            pass    # This indicates command to increment N=0 times, which is a no-op
        elif data == 0b100:
            return str(self.rotor.position)
        elif data == 0b101:
            return self.rotor.__str__()
        elif data == 0b110:
            self.rotor.rotationCounter += 1
            return str(self.rotor.rotationCounter)
        elif data == 0b111:
            print("Client sent exit command")
        elif data > 0b111:
            # This is a command to increment n times
            value = data >> 3   # Discard the opcode bits
            # Use the top bit as a sign bit
            if value & 0b10000:  # If the top bit is 1, the value is negative
                value = -(value & 0b01111)
            print(f"value: {value}")
            if value > 0:
                for i in range(value):
                    self.rotor.increment()
            elif value < 0:
                for i in range(abs(value)):
                    self.rotor.decrement()
            return self.rotor.__str__()
        else:
            raise ValueError(f"Invalid opcode: {data}")
        

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
    server.startTransmission()

    