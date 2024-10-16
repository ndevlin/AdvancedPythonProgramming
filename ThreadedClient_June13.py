
"""
Threaded Client
June 13 2024
"""

import socket
import json
import unittest
import time
from ByteStreams_May15_NDevlin import ByteStream
from Databases_Refactor_May17 import SqliteManager

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import _thread as thread, time
import queue
import threading

global condition
condition = threading.Condition()


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    
    def connect(self):
        self.sock.connect(('localhost', 12346))
        self.connected = True

    def sendMessage(self, message):
        bytestream = ByteStream(message)
        self.sock.sendall(bytestream.get_bytes())
        response = self.sock.recv(1024)
        bytestream = ByteStream(response, isBinary=True)
        return bytestream.get_string()
    
    def interactiveModeStart(self):
        print("Connected to server...")
        try:
            query = ''
            while True:
                query = input("Client: ")
                if query.lower() == 'exit':
                    self.exit()
                    break
                else:
                    result = self.sendMessage(query)
                    if result.lower() == "exit":
                        print("Server exited")
                        print("Closing Connection")
                        self.sock.close()
                        break
                    print("Server:", result)
        except:
            print("Closing Connection")
            self.sock.close()
    
    def sendTextFile(self, filename):
        print("Attempting to send text file ", filename)
        try:
            print("Connected to server...")
            lines = []
            with open(filename, 'r') as file:
                lines = file.readlines()
                print("Beginning to send file")
                for line in lines: 
                    bytestream = ByteStream(line)
                    self.sock.sendall(bytestream.get_bytes())
                    time.sleep(1)
            print("File sent, closing connection")
            bytestream = ByteStream("exit")
            self.sock.sendall(bytestream.get_bytes())
            self.sock.close()
        except:
            print("Error. Closing Connection")
            self.sock.close()
    
    def sendBinaryFile(self, filename):
        print("Attempting to send binary file ", filename)
        print("Connected to server...")
        with open(filename, 'rb') as file:
            print("Beginning to send file")
            bytestream = ByteStream(file.read(), isBinary=True)
            self.sock.sendall(bytestream.get_bytes())
            time.sleep(1)
        print("File sent")

    def exit(self):
        print("Exiting")
        self.sendMessage("exit")
        print("Closing Connection")
        self.sock.close()


class PlotManager:
    def __init__(self, df):
        self.df = df

    def __str__(self):
        return f'PlotManager for DataFrame with {self.df.shape[0]} rows and {self.df.shape[1]} columns'

    def linePlot(self, title=None):
        x, y = self.df.columns[:7]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.plot(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def barPlot(self, title=None):
        x, y = self.df.columns[:7]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.bar(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def scatterPlot(self, title=None):
        x, y = self.df.columns[:7]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.scatter(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def linearRegressionPlot(self, title=None, yLabel="Data Values"):
        x = self.df.columns[0]
        dataColumns = self.df.columns[1:7]

        plt.figure(figsize=(10, 6))  # Set figure size for better readability

        for y in dataColumns:
            if not title:
                title = f'Linear Regression of {y} by {x}'
            # Calculate the linear regression (slope and intercept)
            slope, intercept = np.polyfit(self.df[x], self.df[y], 1)
            # Calculate the y-values based on the slope and intercept
            yVals = slope * self.df[x] + intercept
            # Plot the original data as a scatter plot
            plt.scatter(self.df[x], self.df[y], label=f'Data {y}')
            # Plot the regression line
            plt.plot(self.df[x], yVals, label=f'Linear Regression {y}')

        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(yLabel)
        plt.legend()
        plt.show()


class SqliteManagerLite:
    def queryBuilder(self, query_type, table_name, queryVal1=None, queryVal2=None):
        if query_type.upper() == "CREATE TABLE":
            query_string = f"CREATE TABLE IF NOT EXISTS {table_name} {queryVal1}"
        elif query_type.upper() == "INSERT":
            query_string = f"INSERT INTO {table_name} VALUES {queryVal1}"
        elif query_type.upper() == "SELECT":
            query_string = f"SELECT * FROM {table_name}"
        elif query_type.upper() == "WHERE":
            query_string = f"SELECT {queryVal1} FROM {table_name} WHERE {queryVal2}"
        elif query_type.upper() == "UPDATE":
            query_string = f"UPDATE {table_name} SET {queryVal1}"
        elif query_type.upper() == "DELETE":
            query_string = f"DELETE FROM {table_name} WHERE {queryVal1}"
        else:
            raise ValueError(f"Unsupported query type: {query_type}")
        return query_string


class DataRetrievalThread(threading.Thread):
    def __init__(self, dataTupleIn=None):
        threading.Thread.__init__(self)
        self.dataTuple = dataTupleIn
        self.result = None

    def run(self):
        rowIndex, colIndex, year, header = self.dataTuple
        query = sqliteManagerLite.queryBuilder('WHERE', tableName, header, f"Year='{year}'")
        condition.acquire()
        print("Sending query: " + query)
        result = client.sendMessage(query)
        print("Received result:", result)
        self.result = float(result)
        condition.notify()
        condition.release()


# Main

tableName = "GlobalRadiativeForcing"
headers = ["Year", "C02", "CH4", "N2O", "CFCs", "HCFCs", "HFCs"]
numCols = 7
startYear = 1979
endYear = 2022
numRows = endYear - startYear + 1
years = [str(year) for year in range(startYear, endYear + 1)]
totalCells = numCols * numRows

sqliteManagerLite = SqliteManagerLite()

client = Client()
print("Creating client...")
client.connect()

# Initialize an empty 2D array with dimensions numRows x numCols
dataIn2DForm = np.empty((numRows, numCols))

dataQueryQueue = []

# Create queue of data queries to be processed
for rowIndex, year in enumerate(years):
    for colIndex, header in enumerate(headers):
        if header == "Year":
            dataIn2DForm[rowIndex, colIndex] = int(year)
        else:
            dataQueryQueue.append((rowIndex, colIndex, year, header))

print(dataQueryQueue)

# Create a queue of threads to process the data
threadQueue = queue.Queue()

numThreads = 6
agents = []

while dataQueryQueue != []:
    for i in range(numThreads):
        agent = dataQueryQueue.pop(0)
        agents.append(agent)
    
    for agent in agents:
        thread = DataRetrievalThread(agent)
        threadQueue.put(thread)

    while not threadQueue.empty():
        currThread = threadQueue.get()
        currThread.start()
        currThread.join()
        result = currThread.result
        rowIndex, colIndex, year, header = currThread.dataTuple
        dataIn2DForm[rowIndex, colIndex] = result


# Create the DataFrame
df = pd.DataFrame(dataIn2DForm, columns=headers)
print(df)


plotManager = PlotManager(df)
print(plotManager)
plotManager.linearRegressionPlot("Linear Regression of Global Radiative Forcing By Year", \
                                 "Global Radiative Forcing (W m-2)")


print("Closing client socket...")
client.sock.close()

print("Done")
