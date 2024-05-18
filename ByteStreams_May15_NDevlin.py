
'''
ByteStream class that can be used to convert between strings, bytes, bytearrays, and bitstrings.
May 17, 2024
'''

import bitstring
import socket
import unittest

class ByteStream:
    def __init__(self, data, isBinary=False):
        if data is None:
            self._bytes = b''
            self._bytearray = bytearray()
            self._bitstring = bitstring.BitArray()
            self._string = None
        elif isBinary:
            self._bytes = data
            self._bytearray = bytearray(data)
            self._bitstring = bitstring.BitArray(bytes=data)
            self._string = None
        else:
            self._string = data
            self._bytes = self._string.encode()
            self._bytearray = bytearray(self._string, 'utf-8')
            self._bitstring = bitstring.BitArray(bytes=self._bytes)

    def __str__(self):
        if self._string:
            return self._string 
        else: 
            return self._bytes.decode()

    def __iter__(self):
        if self._string:
            return iter(self._string) 
        else:
            return iter(self._bytes)

    def __len__(self):
        return len(self._bytearray)

    def __getitem__(self, index):
        return self._bytearray[index]

    def __setitem__(self, index, value):
        self._bytearray[index] = value
        self._bytes = bytes(self._bytearray)
        self._bitstring = bitstring.BitArray(self._bytes)
        try:
            self._string = self._bytes.decode()
        except:
            print("string not converted")

    def __contains__(self, item):
        return item in self._bytearray
    
    def set_string(self, value):
        self._bytes = value.encode()
        self._bytearray = bytearray(self._bytes)
        self._bitstring = bitstring.BitArray(self._bytes)
        self._string = value
        return self._bytes
    
    def get_string(self):
        if self._string is not None:
            return self._string
        else:
            return self._bytes.decode()

    def get_bytes(self):
        return self._bytes

    def get_bytearray(self):
        return self._bytearray

    def get_bitstring(self):
        return self._bitstring.bin

    def get_bytesToString(self):
        return self._bytes.decode()

    def get_bytearrayToString(self):
        return bytes(self._bytearray).decode()

    def get_bitstringToString(self):
        return self._bitstring.bytes.decode()

    def get_bitstringTobytes(self):
        return self._bitstring.bytes

    def send_bytestream(self, bytestream, socket):
        conn, _ = socket.accept()
        try:
            conn.sendall(bytestream)
        finally:
            conn.close()

    def receive_bytestream(self, socket):
        conn, _ = socket.accept()
        try:
            return conn.recv(1024)
        finally:
            conn.close()
    

class TestByteStream(unittest.TestCase):
    def setUp(self):
        self.converter = ByteStream("Hello, World!")

    def test_get_string(self):
        self.assertEqual(self.converter.get_string(), "Hello, World!")

    def test_get_bytes(self):
        self.assertEqual(self.converter.get_bytes(), b"Hello, World!")

    def test_get_bytearray(self):
        self.assertEqual(self.converter.get_bytearray(), bytearray(b"Hello, World!"))

    def test_get_bitstring(self):
        self.converter.set_string('A')
        self.assertEqual(self.converter.get_bitstring(), '01000001')
        
    def test_byte_conversion(self):
        byte = self.converter.get_bytes()
        print(f"Testing byte conversion: {byte}")
        self.assertEqual(self.converter.get_bytesToString(), "Hello, World!")
        print("Passed byte conversion test")

    def test_bitstring_conversion(self):
        bitstring = self.converter.get_bitstring()
        print(f"Testing bitstring conversion: {bitstring}")
        self.assertEqual(self.converter.get_bitstringTobytes(), self.converter.get_bytes())
        print("Passed bitstring conversion test")

    def test_len(self):
        print(f"Testing length: {len(self.converter)}")
        self.assertEqual(len(self.converter), 13)
        print("Passed length test")

    def test_getitem(self):
        print(f"Testing get item: {self.converter[0]}")  # ASCII value of 'H'
        self.assertEqual(self.converter[0], 72)
        print("Passed get item test")

    def test_setitem(self):
        print("Testing set item: Setting first item to 74 (ASCII value of 'J')")
        self.converter[0] = 74
        self.assertEqual(self.converter[0], 74)
        self.assertEqual(str(self.converter), "Jello, World!")
        print("Passed set item test")

    def test_contains(self):
        print("Testing contains: Checking if 72 (ASCII value of 'H') is in ByteStream")
        self.assertTrue(72 in self.converter)
        print("Passed contains test for 'H'")
        print("Testing contains: Checking if 74 (ASCII value of 'J') is not in ByteStream")
        self.assertFalse(74 in self.converter)
        print("Passed contains test for 'J'")

    def test_send_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect(('localhost', port))
                print("Testing send byte stream: Sending byte stream")
                self.converter.send_bytestream(self.converter.get_bytes(), s)
                data = clientSocket.recv(1024)
                self.assertEqual(data, self.converter.get_bytes())
                print("Passed send byte stream test")

    def test_receive_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect(('localhost', port))
                clientSocket.sendall(self.converter.get_bytes())
                print("Testing receive byte stream: Receiving byte stream")
                data = self.converter.receive_bytestream(s)
                self.assertEqual(data, self.converter.get_bytes())
                print("Passed receive byte stream test")

# Main
if __name__ == "__main__":
    unittest.main()
    
