import unittest
import socket
import bitstring

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
    


    # Probably wont use:
    def send(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(self._bytes)

    def receive(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()

            # Set a timeout
            s.settimeout(2.0)

            try:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    self._bytes = data
                    self._bytearray = bytearray(data)
                    self._bitstring = bitstring.BitArray(bytes=data)
                    self._string = None
            except socket.timeout:
                print("Socket timed out")
    

class TestByteStream(unittest.TestCase):
    def setUp(self):
        self.converter = ByteStream("Hello, World!")
        print("\nSetup: Created ByteStream with string 'Hello, World!'")

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

    
    # Probably wont use:
    '''
    def test_send_and_receive(self):

        import threading

        # Create an Event to signal when the server has started
        server_started = threading.Event()

        # Start a server in a separate thread
        server_thread = threading.Thread(target=self.start_server, args=(server_started,))
        server_thread.start()

        # Wait for the server to start
        server_started.wait()

        # Send data
        self.converter.send('127.0.0.1', 12345)

        # Wait for the server to finish
        server_thread.join()

    def start_server(self, server_started):
    # Create a new ByteStream object to receive data
        receiver = ByteStream(b'', isBinary=True)

        try:
            # Start listening for connections
            receiver.receive('127.0.0.1', 12345)

            # Signal that the server has started
            server_started.set()

            # Check that the received data matches the sent data
            self.assertEqual(receiver.get_byte(), self.converter.get_byte())
        finally:
            # Close the server socket
            receiver.close()
    '''

unittest.main()
    
