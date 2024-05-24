
"""
Rotator Server
May 24 2024
"""



# Mostly unmodified from original Server

import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager
from RotatorForCommand_May24 import Rotor

class Server:
    def __init__(self, mode="test", db_name="Database.db"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12346))
        self.mode = mode
        if mode == "testSqlQueries":
            self.db = SqliteManager(db_name)
            self.db.executeQuery('CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, name TEXT)')
            self.db.executeQuery("INSERT INTO Database (name) VALUES ('Jack'), ('Jill')")

    def startSqlQueries(self):
        print("SqlQuery Server")
        self.sock.listen(1)
        print("Starting server...")
        while True:
            print("Waiting for connection...")
            conn, addr = self.sock.accept()
            print("Connected...")
            data = conn.recv(1024)
            print("Received data:", data)
            if data:
                response = self.processQuery(data.decode('utf-8'))
                print(f"Response:", response)
                # Convert the result to a list of dictionaries
                result = [{'id': row[0], 'name': row[1]} for row in response]
                # Convert the result to JSON
                jsonResult = json.dumps(result)
                print("Sending response:", jsonResult)
                bytestream = ByteStream(data=jsonResult, isBinary=False)
                conn.sendall(bytestream.get_bytes())
            conn.close()

    def startInteractive(self):
        self.sock.listen(1)
        print("Interactive Chat")
        print("Starting chat...")
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            userInput = ''
            while userInput.lower() != 'exit':
                data = conn.recv(1024)
                if data:
                    response = data.decode('utf-8')
                    print("Client:", response)
                    if response.lower() == 'exit':
                        print("Client exited")
                        break
                    userInput = input("Server: ")
                    bytestream = ByteStream(data=userInput, isBinary=False)
                    conn.sendall(bytestream.get_bytes())
            print("Exiting")
            print("Closing Connection")
            conn.close()
        except:
            print("Closing Connection")
            conn.close()
    

    def startReceiveTextFile(self):
        print("Attempting to Receive Text File")
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            print("Connected...")
            receivedData = ""
            while receivedData.lower() != 'exit':
                data = conn.recv(1024)
                if data:
                    receivedData = data.decode('utf-8')
                    print(receivedData)
                    if receivedData.lower() == 'exit':
                        print("Client exited")
                        break
            print("Closing Connection")
            conn.close()
        except:
            print("Error. Closing Connection")
            conn.close()


    def startReceiveBinaryFile(self, filename="receivedBinaryFile.bin"):
        print("Attempting to Receive Binary File to ", filename)
        self.sock.listen(1)
        print("Waiting for connection...")
        conn, addr = self.sock.accept()
        try:
            print("Connected...")
            receivedData = ""
            data = conn.recv(131072)
            if data:
                receivedData = data.decode('utf-8')
                with open(filename, "w") as file:
                    file.write(receivedData)
                print("Wrote received data to file: ", filename)
            else:
                print("No data received")
            print("Closing Connection")
            conn.close()
        except:
            print("Error. Closing Connection")
            conn.close()

    def processQuery(self, query):
        result = self.db.executeQuery(query)
        return result

if __name__ == '__main__':

    # interactionMode should be set to "interactive", "testSqlQueries", "receiveTextFile", or "receiveBinaryFile"
    interactionMode = "testSqlQueries"

    if interactionMode == "interactive":
        server = Server("interactive")
        server.startInteractive()

    if interactionMode == "testSqlQueries":
        server = Server("testSqlQueries", "Database.db")
        server.startSqlQueries()

    if interactionMode == "receiveTextFile":
        server = Server("receiveTextFile")
        server.startReceiveTextFile()
    
    if interactionMode == "receiveBinaryFile":
        server = Server("receiveBinaryFile")
        filename = "receivedBinaryFile.bin"
        server.startReceiveBinaryFile()

