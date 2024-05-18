"""
Sockets
May 17 2024
"""

import socket
import json
import unittest
import threading
import time
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Server:
    def __init__(self, host='localhost', port=12345, db_name='mydb.db'):
        self.bs = ByteStream(' ')
        self.db = SqliteManager(db_name)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        try:
            self.sock.bind((host, port))
        except socket.error as e:
            print(f"Socket error: {e}")

    def start(self):
        self.running = True
        self.sock.listen(1)
        while self.running:
            try:
                conn, addr = self.sock.accept()
                self.handle_client(conn)
            except Exception as e:
                print(f"Error handling client: {e}")

    def stop(self):
        self.running = False

    def handle_client(self, conn):
        try:
            data = conn.recv(1024)
            self.bs = ByteStream(data, isBinary=True)
            query = self.bs.get_string()
            db = SqliteManager('test.db')  # create a new SqliteManager instance
            result = db.executeQuery(query)  # use the new instance
            result_json = json.dumps(result)  # convert the result to a JSON string
            conn.send(self.bs.set_string(result_json))  # send the JSON string
        except Exception as e:
            print(f"Error in client communication: {e}")

class Client:
    def __init__(self, host='localhost', port=12345):
        self.bs = ByteStream(' ')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")

    def send_query(self, query):
        self.bs.set_string(query)
        self.sock.send(self.bs.get_bytes())
        response = self.sock.recv(1024)
        self.bs = ByteStream(response, isBinary=True)
        response_string = self.bs.get_string()
        if response_string:
            return json.loads(response_string)
        else:
            print("Received empty response from server")
            return None


class TestServerClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Server(db_name='test.db')
        cls.server_thread = threading.Thread(target=cls.server.start)
        cls.server_thread.start()
        time.sleep(4)  # increase the delay to give the server more time to start
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()  # stop the server
        time.sleep(1)  # wait for the server to finish handling requests
        cls.server.sock.close()
        cls.client.sock.close()
        cls.server_thread.join()

    def test_query(self):
        db = SqliteManager('test.db')
        db.executeQuery('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
        db.executeQuery("INSERT INTO test (name) VALUES ('Alice'), ('Bob')")

        result = self.client.send_query('SELECT * FROM test')
        self.assertEqual(result, [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}])

if __name__ == '__main__':
    unittest.main()

