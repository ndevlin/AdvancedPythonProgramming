import socket
import json
import unittest
import time
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self):
        self.sock.connect(('localhost', 12345))
        self.connected = True

    def sendMessage(self, message):
        bytestream = ByteStream(message)
        self.sock.sendall(bytestream.get_bytes())
        response = self.sock.recv(1024)
        bytestream = ByteStream(response, isBinary=True)
        return bytestream.get_string()
    
    def exit(self):
        print("Exiting")
        self.sendMessage("exit")
        print("Closing Connection")
        self.sock.close()

class TestServerClient(unittest.TestCase):
    def testQuery(self):
        client = Client()
        print("Creating client...")
        client.connect()
        try:
            print("Sending query: 'SELECT * FROM Database'")
            result = client.sendMessage('SELECT * FROM Database')
            print(f"Received result: {result}")
            self.assertEqual(json.loads(result), [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}])
        except Exception as e:
            print(f"Error sending query: {e}")
        finally:
            print("Closing client socket...")
            client.sock.close()

if __name__ == '__main__':

    # Mode should equal "interactive" or "test"
    mode = "test"

    if mode == "test":
        unittest.main()

    
    if mode == "interactive":
        client = Client()
        client.connect()
        client.connected = True
        print("Connected to server...")
        try:
            query = ''
            while True:
                query = input("Client: ")
                if query.lower() == 'exit':
                    client.exit()
                    break
                else:
                    result = client.sendMessage(query)
                    if result.lower() == "exit":
                        print("Server exited")
                        print("Closing Connection")
                        client.sock.close()
                        break
                    print(f"Server: {result}")
        except:
            print("Closing Connection")
            client.sock.close()

