import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Server:
    def __init__(self, db_name):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12346))
        self.db = SqliteManager(db_name)

    def start(self):
        self.sock.listen(1)
        print("Starting server...")
        while True:
            print("Waiting for connection...")
            conn, addr = self.sock.accept()
            print("Connected...")
            data = conn.recv(1024)
            print(f"Received data: {data}")
            if data:
                response = self.processQuery(data.decode('utf-8'))
                print(f"Response: {response}")
                # Convert the result to a list of dictionaries
                result = [{'id': row[0], 'name': row[1]} for row in response]
                # Convert the result to JSON
                json_result = json.dumps(result)
                print(f"Sending response: {json_result}")
                byte_stream = ByteStream(data=json_result, isBinary=False)
                conn.sendall(byte_stream.get_bytes())
            conn.close()

    def processQuery(self, query):
        result = self.db.executeQuery(query)
        return result

if __name__ == '__main__':
    db = SqliteManager('Database.db')
    db.executeQuery('CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, name TEXT)')
    db.executeQuery("INSERT INTO Database (name) VALUES ('Alice'), ('Bob')")
    server = Server('Database.db')
    server.start()
