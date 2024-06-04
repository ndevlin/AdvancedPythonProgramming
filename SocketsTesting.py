
import json
import unittest
import time
from Client_RefactorJun3 import Client

class TestSockets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        print("Creating client...")
        cls.client.connect()


    def testQuery(self):
        print("Sending query: 'SELECT * FROM Database'")
        result = self.client.sendMessage('SELECT * FROM Database')
        print("Received result:", result)
        # Test that the returned entry starts with the expected first two entries
        self.assertEqual(json.loads(result)[:2], [{'id': 1, 'name': 'Jack'}, {'id': 2, 'name': 'Jill'}])


    def testSendBinaryFile(self):
        with open("testBinaryFile.bin", 'wb') as file:
            textString = "This is a test binary string"
            binaryData = textString.encode('utf-8') 
            file.write(binaryData)
        self.client.sendBinaryFile("testBinaryFile.bin")
        with open("testBinaryFile.bin", 'rb') as sent_file, open("receivedBinaryFile.bin", 'rb') as received_file:
            sent_data = sent_file.read()
            received_data = received_file.read()
            self.assertEqual(sent_data, received_data, "The sent and received binary files are not the same.")


    def testSendTextFile(self):
        filename = "Sockets_TestText_June3.txt"
        self.client.sendTextFile(filename)

        expectedText = """To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them."""
        time.sleep(10) # Wait for the server to finish writing the file
        with open("receivedTextFile.txt", 'r') as receivedFile:
            receivedText = receivedFile.read()
            self.assertEqual(receivedText, expectedText, "The received text file does not match the expected text.")

        self.client.sock.close()


if __name__ == '__main__':
    unittest.main()
