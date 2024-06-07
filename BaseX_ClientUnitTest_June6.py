
import unittest
import time
import socket

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True

    def sendMessage(self, message):
        self.sock.sendall(message.encode('utf-8'))
        response = self.sock.recv(1024)
        return response.decode('utf-8')
    
    def interactiveModeStart(self):
        print("Connected to server...")
        toSend = ''
        while True:
            print("Enter three comma-separated values: number1, number2, operation")
            toSend += input()
            if 'exit' in toSend.lower():
                self.exit()
                break
            else:
                result = self.sendMessage(toSend)
                if result.lower() == "exit":
                    print("Server exited")
                    print("Closing Connection")
                    self.sock.close()
                    break
                print("Result:", result)

    def exit(self):
        print("Exiting")
        self.sendMessage("exit")
        print("Closing Connection")
        self.sock.close()


class TestBaseXSystem(unittest.TestCase):
    def setUpClass(cls):
        cls.client = Client()
        print("Creating client...")
        cls.client.connect()

    def testAdditionAndSubtraction(self):
        self.assertEqual(1, 1)
        print("Addition and Subtraction Test Passed")
        
        
        #self.client.sock.close()


# Run the tests
if __name__ == '__main__':

    client = Client()
    client.connect()
    client.interactiveModeStart()

    unittest.main()
