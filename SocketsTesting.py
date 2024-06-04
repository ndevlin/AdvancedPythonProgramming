
import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager
import unittest
import time
from Client_RefactorJun3 import Client
from Server_May21 import Server

class TestSockets(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        print("Creating client...")
        self.client.connect()


    def testQuery(self):
        try:
            print("Sending query: 'SELECT * FROM Database'")
            result = self.client.sendMessage('SELECT * FROM Database')
            print("Received result:", result)
            # Test that the returned entry starts with the expected first two entries
            self.assertEqual(json.loads(result)[:2], [{'id': 1, 'name': 'Jack'}, {'id': 2, 'name': 'Jill'}])
        except Exception as e:
            print(f"Error sending query: {e}")

    '''
    def testInteractiveMode(self):
        self.client.interactiveModeStart()
        # Add assertions here to verify the interactive mode

    def testSendTextFile(self):
        filename = "Sockets_TestText_May21.txt"
        self.client.sendTextFile(filename)
        # Add assertions here to verify the text file was sent correctly

    def testSendBinaryFile(self):
        with open("testBinaryFile.bin", 'wb') as file:
            textString = "This is a test binary string"
            binaryData = textString.encode('utf-8') 
            file.write(binaryData)
        self.client.sendBinaryFile("testBinaryFile.bin")
        # Add assertions here to verify the binary file was sent correctly

        self.client.sock.close()
    '''

if __name__ == '__main__':
    unittest.main()
