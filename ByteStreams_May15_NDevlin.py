import binascii
import unittest
import socket

class ByteStream:
    def __init__(self, data, is_binary=False):
        if is_binary:
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

    def test_byte_conversion(self):
        byte = self.converter.get_byte()
        self.assertEqual(self.converter.byte_to_string(byte), "Hello, World!")

    def test_byte_array_conversion(self):
        byte_array = self.converter.get_byte_array()
        self.assertEqual(self.converter.byte_array_to_string(byte_array), "Hello, World!")

    def test_bitstring_conversion(self):
        bitstring = self.converter.get_bitstring()
        self.assertEqual(self.converter.bitstring_to_string(bitstring), "Hello, World!")

    
    def test_send_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('localhost', port))
                self.converter.send_byte_stream(self.converter.get_byte(), s)
                data = client_socket.recv(1024)
                self.assertEqual(data, self.converter.get_byte())

    def test_receive_byte_stream(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))  # Bind to a free port
            s.listen()
            _, port = s.getsockname()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('localhost', port))
                client_socket.sendall(self.converter.get_byte())
                data = self.converter.receive_byte_stream(s)
                self.assertEqual(data, self.converter.get_byte())


if __name__ == '__main__':
    unittest.main()
    
