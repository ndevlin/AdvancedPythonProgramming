import sqlite3
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup

import os
import re
import unittest

import numpy as np
import pandas as pd

class WebScraper():

    def __init__(self):
        self.soup = None
        self.memberDict = defaultdict(list)

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
            output.append(str((tagResult)[i].text))

        return (tagIn, tuple(output))

    def cleanTags(self, tagTupleIn):
        self.memberDict[tagTupleIn[0]] = tagTupleIn[1]

    def getData(self):
        return self.memberDict.items()
    
    def convertToTable(self):
        if self.memberDict == defaultdict(list):
            print("Must Clean Tags before converting to Pandas DataFrame")
            return
        
        headers = self.memberDict["tr"][0]
        numRows = int(re.search(r'\n(\d+)\n', self.memberDict["tr"][-1]).group(1))
        headers = headers.split("\n")
        while "" in headers:
            headers.remove("")
        numCols = len(headers)
        pandaReadyList = []
        for i in range(numRows):
            row = []
            for j in range(numCols):
                currVal = i * numCols + j
                row.append(self.memberDict["td"][currVal])
            pandaReadyList.append(row)
        self.dataFrame = pd.DataFrame(pandaReadyList, columns = headers)


class SqliteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(f"Disconnected from database: {self.db_name}")

    def query_builder(self, query_type, table_name, query_tuple=None):
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

    def execute_query(self, query_string):
        try:
            self.cursor.execute(query_string)
            self.conn.commit()
            print(f"Executed query: {query_string}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

def create_sample_database(databaseName='my_database.db'):
    
    # Connect to the SQLite database
    # If the database does not exist, it will be created
    conn = sqlite3.connect(databaseName)

    # Create a cursor object
    c = conn.cursor()

    # Create a table
    c.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
            id TEXT,
            name TEXT,
            photo TEXT,
            html TEXT
        )
    ''')

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


#Main

webScraper = WebScraper()

webScraper.webPageFromFile("Co2TestVersion.html")

relevantTags = ["tr", "td"]

for tag in relevantTags:
    tableData = webScraper.extractTags(tag, 9)  # Skip the first 9 tags which are just a heading
    webScraper.cleanTags(tableData)

numCols = 7
    

#print("Creating sample database...")
#create_sample_database("my_database.db")

databaseName = "my_database.db"

# Connect to the SQLite database
# If the database does not exist, it will be created
conn = sqlite3.connect(databaseName)

# Create a cursor object
c = conn.cursor()

# Commit the transaction
conn.commit()

# Close the connection
conn.close()


with SqliteManager('my_database.db') as db:
    # Test CREATE TABLE
    create_table_query = db.query_builder('CREATE TABLE', 'TotalCarbonEmissions', '(year INTEGER, month INTEGER, decimal FLOAT, average FLOAT, interpolated FLOAT, trend FLOAT, days INTEGER)')
    db.execute_query(create_table_query)

    
    listOfRows = []
    for i in range(0, len(webScraper.memberDict["td"]), numCols):
        listOfRows.append(webScraper.memberDict["td"][i:i+numCols])
    # INSERT
    for row in listOfRows:
        insert_query = db.query_builder('INSERT', 'TotalCarbonEmissions', row)
        db.execute_query(insert_query)

    # Test SELECT
    select_query = db.query_builder('SELECT', 'TotalCarbonEmissions')
    db.execute_query(select_query)

    # Test WHERE
    where_query = db.query_builder('WHERE', 'TotalCarbonEmissions', "year='1959'")
    db.execute_query(where_query)

    # Test UPDATE
    update_query = db.query_builder('UPDATE', 'TotalCarbonEmissions', "year='1958' WHERE year='1959'")
    db.execute_query(update_query)

    # Test DELETE
    delete_query = db.query_builder('DELETE', 'TotalCarbonEmissions', "year='1960'")
    db.execute_query(delete_query)

