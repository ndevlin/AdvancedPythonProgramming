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

    def sendQuery(self, query):
        if not self.connected:
            self.sock.connect(('localhost', 12346))
            self.connected = True
        byte_stream = ByteStream(None)
        byte_stream.set_string(query)
        self.sock.sendall(byte_stream.get_bytes())
        response = self.sock.recv(1024)
        byte_stream = ByteStream(response, isBinary=True)
        return byte_stream.get_string()

class TestServerClient(unittest.TestCase):
    def testQuery(self):
        client = Client()
        print("Creating client...")
        try:
            print("Sending query: 'SELECT * FROM Database'")
            result = client.sendQuery('SELECT * FROM Database')
            print(f"Received result: {result}")
            self.assertEqual(json.loads(result), [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}])
        except Exception as e:
            print(f"Error sending query: {e}")
        finally:
            print("Closing client socket...")
            client.sock.close()

if __name__ == '__main__':

    # Mode should equal "interactive", "test", or "binary"
    mode = "interactive"

    if mode == "test":
        unittest.main()

    
    if mode == "interactive":
        client = Client()
        while True:
            print("Enter a query:")
            query = input()
            result = client.sendQuery(query)
            print(f"Result: {result}")

