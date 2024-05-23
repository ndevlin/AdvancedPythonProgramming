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
        self.sock.connect(('localhost', 12346))
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
            # Test that the returned entry starts with the expected first two entries
            self.assertEqual(json.loads(result)[:2], [{'id': 1, 'name': 'Jack'}, {'id': 2, 'name': 'Jill'}])
        except Exception as e:
            print(f"Error sending query: {e}")
        finally:
            print("Closing client socket...")
            client.sock.close()

if __name__ == '__main__':

    # Mode should equal "interactive", "test", or "interactiveFromTextFile"
    mode = "sendTextFile"

    if mode == "test":
        unittest.main()

    if mode == "interactive":
        client = Client()
        client.connect()
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
    
    
    if mode == "sendTextFile":
        filename = "Sockets_TestText_May21.txt"
        lines = []
        client = Client()
        print("Attempting to send text file ", filename)
        try:
            client.connect()
            print("Connected to server...")
            with open(filename, 'r') as file:
                lines = file.readlines()
                print("Beginning to send file")
                for line in lines: 
                    bytestream = ByteStream(line)
                    client.sock.sendall(bytestream.get_bytes())
                    time.sleep(1)
            print("File sent, closing connection")
            bytestream = ByteStream("File sent, Client closing connection")
            client.sock.sendall(bytestream.get_bytes())
            time.sleep(1)
            bytestream = ByteStream("exit")
            client.sock.sendall(bytestream.get_bytes())
            client.sock.close()
        except:
            print("Error. Closing Connection")
            client.sock.close()

