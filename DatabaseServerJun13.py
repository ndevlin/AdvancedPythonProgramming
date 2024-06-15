
"""
Nathan Devlin
June 13 2024
Threaded Database Server
"""

import sqlite3
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup

import socket
import json
from ByteStreams_May15_NDevlin import ByteStream

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class WebScraper():

    def __init__(self):
        self.soup = None
        self.memberDict = defaultdict(list)
        self.dataFrame = None

    def requestWebPage(self, pageIn):
        try:
            html = urlopen(pageIn)
            self.soup =  BeautifulSoup(html, "html.parser")
        except:
            print("Issue retrieving Web Page")
            self.soup = None

    def webPageFromFile(self, fileName):
        try:
            with open(fileName, "r") as file:
                html = file.read()
                self.soup =  BeautifulSoup(html, "html.parser")
        except:
            print("Issue retrieving Web Page")
            self.soup = None

    def extractTags(self, tagIn, startAt=0):
        if self.soup == None:
            print("Webpage was not loaded")
            return
        
        tagResult = None
        tagResult = self.soup.select(tagIn)
        if tagResult == None:
            print("No tags were found")
            return

        output = []

        for i in range(startAt, len(tagResult)):
            output.append(str((tagResult)[i].text).lstrip("#"))

        return (tagIn, tuple(output))

    def cleanTags(self, tagTupleIn):
        self.memberDict[tagTupleIn[0]] = tagTupleIn[1]

    def getData(self):
        return self.memberDict.items()
    
    def convertToPandasDataFrame(self, headers):
        if self.memberDict == defaultdict(list):
            print("Must Clean Tags before converting to Pandas DataFrame")
            return

        numRows = 44

        numCols = 7

        pandaReadyList = []
        for i in range(numRows):
            row = []
            for j in range(numCols):
                currVal = i * numCols + j
                value = self.memberDict["td"][currVal]
                if type(value) == str:
                    value = float(value)
                row.append(value)
            pandaReadyList.append(row)
        self.dataFrame = pd.DataFrame(pandaReadyList, columns = headers)
        
        return self.dataFrame
    
    def printDataFrame(self):
        print(self.dataFrame)
    

class SqliteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print(f"Disconnected from database: {self.db_name}")

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

    def executeQuery(self, query_string):
        try:
            self.cursor.execute(query_string)
            self.connection.commit()
            print(f"Executed query: {query_string}")
            if query_string.split()[0].upper() == "SELECT" or query_string.split()[0].upper() == "WHERE":
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


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
    

    def close(self):
        print("Closing Connection")
        self.conn.close()






"""
Will later go on Client side
"""

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


    def linearRegressionPlot(self, title=None):
        x = self.df.columns[0]  # Year column
        data_columns = self.df.columns[1:7]  # The next 6 columns with data

        plt.figure(figsize=(10, 6))  # Set figure size for better readability

        for y in data_columns:
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

        plt.title('Linear Regression by Year')
        plt.xlabel(x)
        plt.ylabel('Data Values')
        plt.legend()
        plt.show()



# Main
# Scrape Co2.html to get the data to put in the database
webScraper = WebScraper()

pageIn = 'https://gml.noaa.gov/aggi/aggi.html'

webScraper.requestWebPage(pageIn)

tagsToSkip = 26     # Skip the first 26 tags which are from the previous table
tableData = webScraper.extractTags("td", tagsToSkip)
webScraper.cleanTags(tableData)

originalColLength = 11
numCols = 7
numRows = 44
newTableData = []

# Take only first 7 columns
for i in range(0, originalColLength * numRows, originalColLength):
    newTableData.extend(tableData[1][i:i+numCols])

webScraper.memberDict["td"] = tuple(newTableData)

headers = ["Year", "C02", "CH4", "N2O", "CFCs", "HCFCs", "HFCs"]
i = 0

headerTypes = ["INTEGER", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]
tableTupleData = "("
for header, headerType in zip(headers, headerTypes):
    tableTupleData += header + " " + headerType + ", "
tableTupleData = tableTupleData[:-2] + ")"

databaseName = "GlobalRadiativeForcing.db"
tableName = databaseName.split(".")[0]






# Convert to Pandas DataFrame and print it - not to be used in final version
dataFrame = webScraper.convertToPandasDataFrame(headers)
print(dataFrame)





with SqliteManager(databaseName) as db:

    # Check if the table exists and delete it if it does
    db.executeQuery(f"DROP TABLE IF EXISTS {tableName}")

    # Create Table
    createTableQuery = db.queryBuilder('CREATE TABLE', tableName, tableTupleData)
    db.executeQuery(createTableQuery)

    # Add data to the table
    listOfRows = []
    for i in range(0, len(webScraper.memberDict["td"]), numCols):
        listOfRows.append(webScraper.memberDict["td"][i:i+numCols])

    years = [row[0] for row in listOfRows]

    # INSERT
    for row in listOfRows:
        insert_query = db.queryBuilder('INSERT', tableName, row)
        db.executeQuery(insert_query)


    '''
    # Test SELECT
    select_query = db.queryBuilder('SELECT', tableName)
    db.executeQuery(select_query)

    # Test WHERE
    where_query = db.queryBuilder('WHERE', tableName, "year='1979'")
    db.executeQuery(where_query)
    '''

    nextData = None
    # Queue next query
    for year in years:
        for header in headers:
            if header == "Year":
                nextData = year
                print(nextData)
                continue
            query = db.queryBuilder('WHERE', tableName, header, f"Year='{year}'")
            nextData = db.executeQuery(query)
            nextData = nextData[0][0]   # Extract the string value
            print(nextData)
            






plotManager = PlotManager(dataFrame)
print(plotManager)
plotManager.linearRegressionPlot()

print("Done")




# Server Code
server = Server(databaseName)
server.startSqlQueries()
server.close()

