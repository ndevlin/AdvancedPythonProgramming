import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Server:
    def __init__(self, mode="test", db_name="Database.db"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12345))
        self.mode = mode
        if mode == "test":
            self.db = SqliteManager(db_name)
            self.db.executeQuery('CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, name TEXT)')
            self.db.executeQuery("INSERT INTO Database (name) VALUES ('Jack'), ('Jill')")

    def startText(self):
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

    def startInteractive(self):
        self.sock.listen(1)
        print("Starting chat...")
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            userInput = ''
            while userInput.lower() != 'exit':
                data = conn.recv(1024)
                if data:
                    response = data.decode('utf-8')
                    print(f"Client: {response}")
                    if response.lower() == 'exit':
                        print("Client exited")
                        break
                    userInput = input("Server: ")
                    byte_stream = ByteStream(data=userInput, isBinary=False)
                    conn.sendall(byte_stream.get_bytes())
            print("Exiting")
            print("Closing Connection")
            conn.close()
        except:
            print("Closing Connection")
            conn.close()

    def processQuery(self, query):
        result = self.db.executeQuery(query)
        return result

if __name__ == '__main__':

    # interactionMode should be set to "interactive" or "test"
    interactionMode = "interactive"

    if interactionMode == "interactive":
        server = Server("interactive")
        server.startInteractive()


    if interactionMode == "test":
        server = Server("test", "Database.db")
        server.startText()
