
import unittest
import socket

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True
        print("Connected to server...")

    def sendMessage(self, message):
        self.sock.sendall(message.encode('utf-8'))
        response = self.sock.recv(1024)
        return response.decode('utf-8')

    def exit(self):
        print("Exiting")
        self.sendMessage("exit")
        print("Closing Connection")
        self.sock.close()


class TestBaseXSystem(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        print("Creating client...")
        self.client.connect()

    def testAdditionAndSubtraction(self):
        
        # You could change the values of bP and bJ to test different values
        print("Note that the default of bP is 678 in decimal form, and bJ is 3408 in decimal form")
        bP = "0P_123"
        bPInDecimal = 678
        bJ = "0J_987"
        bJInDecimal = 3408
        print("Add and Subtract Test")
        print(f'Adding bp, {bP} and bj, {bJ}')
        
        print("Add bP and bJ")
        toSend = bP + "," + bJ + ",add"
        print("Send '", toSend, "' to server")
        result = self.client.sendMessage(toSend)
        print("Result:", result)
        print("Subtract bJ from the result")
        toSend = result + "," + bJ + ",sub"
        print("Send '", toSend, "' to server")
        result = self.client.sendMessage(toSend)
        print("Result:", result)
        
        # Convert the result to a decimal int
        result = int(result.split('_')[1])
        print(bPInDecimal, "==", result, "?")
        self.assertEqual(bPInDecimal, result)
        print("Addition and Subtraction Test Passed")
        
        self.client.exit()


# Run the tests
if __name__ == '__main__':

    print("Run the Server/Client based tests: ")

    unittest.main()

    print("Done")
