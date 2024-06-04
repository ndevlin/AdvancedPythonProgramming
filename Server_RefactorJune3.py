
"""
Server
June 3 2024
"""

import socket
import json
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

class Server:
    def __init__(self, db_name="Database.db"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 12346))
        self.db = SqliteManager(db_name)
        self.db.executeQuery('CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, name TEXT)')
        self.db.executeQuery("INSERT INTO Database (name) VALUES ('Jack'), ('Jill')")

        self.sock.listen(1)
        print("Starting server...")
        print("Waiting for connection...")
        self.conn, addr = self.sock.accept()
        print("Connected...")

    def startSqlQueries(self):
        data = self.conn.recv(1024)
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
            self.conn.sendall(bytestream.get_bytes())
    
    def processQuery(self, query):
        result = self.db.executeQuery(query)
        return result

    def startInteractive(self):
        print("Interactive Chat")
        try:
            userInput = ''
            while userInput.lower() != 'exit':
                data = self.conn.recv(1024)
                if data:
                    response = data.decode('utf-8')
                    print("Client:", response)
                    if response.lower() == 'exit':
                        print("Client exited")
                        break
                    userInput = input("Server: ")
                    bytestream = ByteStream(data=userInput, isBinary=False)
                    self.conn.sendall(bytestream.get_bytes())
            print("Exiting")
            print("Closing Connection")
            self.conn.close()
        except:
            print("Closing Connection")
            self.conn.close()
    

    def startReceiveTextFile(self):
        print("Attempting to Receive Text File")
        receivedData = ""
        while receivedData.lower() != 'exit':
            data = self.conn.recv(1024)
            if data:
                receivedData = data.decode('utf-8')
                print(receivedData)
                if receivedData.lower() == 'exit':
                    print("Client exited")
                    break



    def startReceiveBinaryFile(self, filename="receivedBinaryFile.bin"):
        print("Attempting to Receive Binary File to ", filename)
        receivedData = ""
        data = self.conn.recv(131072)
        if data:
            receivedData = data.decode('utf-8')
            with open(filename, "w") as file:
                file.write(receivedData)
            print("Wrote received data to file: ", filename)
        else:
            print("No data received")

    def close(self):
        print("Closing Connection")
        self.conn.close()

if __name__ == '__main__':

    server = Server("Database.db")
    server.startSqlQueries()
    server.startReceiveBinaryFile()
    server.startReceiveTextFile()
    server.close()
