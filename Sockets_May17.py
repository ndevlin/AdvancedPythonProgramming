"""
Sockets
May 17 2024
"""

import socket
import json
import unittest
import time
import threading
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Server:
    def __init__(self, host='localhost', port=12345, db_name='mydb.db'):
        self.bytestream = ByteStream(' ')
        self.db = SqliteManager(db_name)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        try:
            self.sock.bind((host, port))
        except socket.error as e:
            print("Socket error: ", e)

    def start(self):
        self.running = True
        self.sock.listen(1)
        while self.running:
            try:
                conn, addr = self.sock.accept()
                self.handleClient(conn)
            except Exception as e:
                print("Error with client: ", e)

    def stop(self):
        self.running = False

    def handleClient(self, conn):
        try:
            data = conn.recv(1024)
            self.bytestream = ByteStream(data, isBinary=True)
            query = self.bytestream.get_string()
            db = SqliteManager('Database.db')  # create a new SqliteManager instance
            result = db.executeQuery(query)  # use the new instance
            resultJson = json.dumps(result)  # convert the result to a JSON string
            conn.send(self.bytestream.set_string(resultJson))  # send the JSON string
        except Exception as e:
            print("Error in client communication: ", e)

class Client:
    def __init__(self, host='localhost', port=12345):
        self.bytestream = ByteStream(' ')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except socket.error as e:
            print("Error connecting to server: ", e)

    def sendQuery(self, query):
        self.bytestream.set_string(query)
        self.sock.send(self.bytestream.get_bytes())
        response = self.sock.recv(1024)
        self.bytestream = ByteStream(response, isBinary=True)
        responseString = self.bytestream.get_string()
        if responseString:
            return json.loads(responseString)
        else:
            print("Received empty response from server")
            return None


class TestServerClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Server(db_name='Database.db')
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

    def testQuery(self):
        db = SqliteManager('Database.db')
        db.executeQuery('CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, name TEXT)')
        db.executeQuery("INSERT INTO Database (name) VALUES ('Alice'), ('Bob')")

        result = self.client.sendQuery('SELECT * FROM Database')
        self.assertEqual(result, [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}])

if __name__ == '__main__':
    unittest.main()

