
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

import pandas as pd

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
    
    def convertToPandasDataFrame(self):
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
                row.append(self.memberDict["td"][currVal])
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

    def queryBuilder(self, query_type, table_name, query_tuple=None):
        if query_type.upper() == "CREATE TABLE":
            query_string = f"CREATE TABLE IF NOT EXISTS {table_name} {query_tuple}"
        elif query_type.upper() == "INSERT":
            query_string = f"INSERT INTO {table_name} VALUES {query_tuple}"
        elif query_type.upper() == "SELECT":
            query_string = f"SELECT * FROM {table_name}"
        elif query_type.upper() == "WHERE":
            query_string = f"SELECT * FROM {table_name} WHERE {query_tuple}"
        elif query_type.upper() == "UPDATE":
            query_string = f"UPDATE {table_name} SET {query_tuple}"
        elif query_type.upper() == "DELETE":
            query_string = f"DELETE FROM {table_name} WHERE {query_tuple}"
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

import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, df):
        self.df = df

    def __str__(self):
        return f'PlotManager for DataFrame with {self.df.shape[0]} rows and {self.df.shape[1]} columns'

    def linePlot(self, title=None):
        x, y = self.df.columns[:2]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.plot(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def barPlot(self, title=None):
        x, y = self.df.columns[:2]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.bar(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def scatterPlot(self, title=None):
        x, y = self.df.columns[:2]
        if not title:
            title = f'{y} by {x}'
        plt.figure()
        plt.scatter(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
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

with SqliteManager(databaseName) as db:
    # Test CREATE TABLE
    create_table_query = db.queryBuilder('CREATE TABLE', tableName, tableTupleData)
    db.executeQuery(create_table_query)

    listOfRows = []
    for i in range(0, len(webScraper.memberDict["td"]), numCols):
        listOfRows.append(webScraper.memberDict["td"][i:i+numCols])
    # INSERT
    for row in listOfRows:
        insert_query = db.queryBuilder('INSERT', tableName, row)
        db.executeQuery(insert_query)

    # Test SELECT
    select_query = db.queryBuilder('SELECT', tableName)
    db.executeQuery(select_query)

    # Test WHERE
    where_query = db.queryBuilder('WHERE', tableName, "year='1979'")
    db.executeQuery(where_query)


originalDataFrame = webScraper.convertToPandasDataFrame()
print(originalDataFrame)

'''
# Convert the 'Greenhouse gas emissions from agriculture' column from string to numeric
originalDataFrame['Greenhouse gas emissions from agriculture'] = pd.to_numeric(originalDataFrame['Greenhouse gas emissions from agriculture'], errors='coerce')
# Group each country with the agriculture emissions
countryData = originalDataFrame.groupby('Entity')['Greenhouse gas emissions from agriculture']
# Take the average
averageEmissions = countryData.mean()
# Create a new dataframe with that data
averageEmissionsDataFrame = averageEmissions.reset_index()
# Rename the columns
averageEmissionsDataFrame.columns = ['Country', 'Average Agriculture Emissions']
#display_dataframe(averageEmissionsDataFrame, title="Average Agricultural Emissions By Country")
'''




# Server Code
server = Server(databaseName)
server.startSqlQueries()
server.close()

