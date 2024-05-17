import binascii
import unittest
import socket

class ByteStream:
    def __init__(self, data, isBinary=False):
        if isBinary:
            self._byte = data
            self._byte_array = bytearray(data)
            self._bitstring = bin(int(binascii.hexlify(self._byte), 16))
            self._string = None
        else:
            self._string = data
            self._byte = self._string.encode()
            self._byte_array = bytearray(self._string, 'utf-8')
            self._bitstring = bin(int(binascii.hexlify(self._byte), 16))

    def __str__(self):
        return self._string if self._string else self._byte.decode()

    def __iter__(self):
        return iter(self._string) if self._string else iter(self._byte)

    def __len__(self):
        return len(self._byte_array)

    def __getitem__(self, index):
        return self._byte_array[index]

    def __setitem__(self, index, value):
        self._byte_array[index] = value
        self._byte = bytes(self._byte_array)
        self._bitstring = bin(int(binascii.hexlify(self._byte), 16))
        try:
            self._string = self._byte.decode()
        except:
            print("Decode error")

    def __contains__(self, item):
        return item in self._byte_array

    def get_byte(self):
        return self._byte

    def get_byte_array(self):
        return self._byte_array

    def get_bitstring(self):
        return self._bitstring

    def byte_to_string(self, byte):
        return byte.decode()

    def byte_array_to_string(self, byte_array):
        return byte_array.decode()

    def bitstring_to_string(self, bitstring):
        n = int(bitstring, 2)
        return binascii.unhexlify('%x' % n).decode()

    def bitstring_to_byte(self, bitstring):
        byte_string = int(bitstring, 2).to_bytes((len(bitstring) + 7) // 8, 'big')
        return byte_string.lstrip(b'\x00')

    def send_byte_stream(self, byte_stream, socket):
        conn, _ = socket.accept()
        try:
            conn.sendall(byte_stream)
        finally:
            conn.close()

    def receive_byte_stream(self, socket):
        conn, _ = socket.accept()
        try:
            return conn.recv(1024)
        finally:
            conn.close()
    

class TestByteStream(unittest.TestCase):
    def setUp(self):
        self.converter = ByteStream("Hello, World!")
        print("\nSetup: Created ByteStream with string 'Hello, World!'")

    def test_byte_conversion(self):
        byte = self.converter.get_byte()
        print(f"Testing byte conversion: {byte}")
        self.assertEqual(self.converter.byte_to_string(byte), "Hello, World!")
        print("Passed byte conversion test")

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

    def test_bitstring_conversion(self):
        bitstring = self.converter.get_bitstring()
        print(f"Testing bitstring conversion: {bitstring}")
        self.assertEqual(self.converter.bitstring_to_byte(bitstring), self.converter.get_byte())
        print("Passed bitstring conversion test")

    def test_send_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect(('localhost', port))
                print("Testing send byte stream: Sending byte stream")
                self.converter.send_byte_stream(self.converter.get_byte(), s)
                data = clientSocket.recv(1024)
                self.assertEqual(data, self.converter.get_byte())
                print("Passed send byte stream test")

    def test_receive_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect(('localhost', port))
                clientSocket.sendall(self.converter.get_byte())
                print("Testing receive byte stream: Receiving byte stream")
                data = self.converter.receive_byte_stream(s)
                self.assertEqual(data, self.converter.get_byte())
                print("Passed receive byte stream test")


unittest.main()
    
