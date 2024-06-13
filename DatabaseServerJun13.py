
"""
Nathan Devlin
June 13 2024
Threaded Database Server
"""

import sqlite3
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
            output.append(str((tagResult)[i].text).lstrip("#"))

        return (tagIn, tuple(output))

    def cleanTags(self, tagTupleIn):
        self.memberDict[tagTupleIn[0]] = tagTupleIn[1]

    def getData(self):
        return self.memberDict.items()
    

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


# Main
# Scrape Co2.html to get the data to put in the database
webScraper = WebScraper()

webScraper.webPageFromFile("Co2.html")

tableData = webScraper.extractTags("td", 2)  # Skip the first 2 tags which are just a heading
webScraper.cleanTags(tableData)

numCols = 7
headers = []
i = 0
headers = webScraper.memberDict["td"][0:numCols]
webScraper.memberDict["td"] = webScraper.memberDict["td"][numCols:]

headerTypes = ["INTEGER", "INTEGER", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "INTEGER"]
tableTupleData = "("
for header, headerType in zip(headers, headerTypes):
    tableTupleData += header + " " + headerType + ", "
tableTupleData = tableTupleData[:-2] + ")"

databaseName = "GlobalRadiativeForcing.db"

with SqliteManager(databaseName) as db:
    # Test CREATE TABLE
    create_table_query = db.queryBuilder('CREATE TABLE', 'TotalCarbonEmissions', tableTupleData)
    db.executeQuery(create_table_query)

    listOfRows = []
    for i in range(0, len(webScraper.memberDict["td"]), numCols):
        listOfRows.append(webScraper.memberDict["td"][i:i+numCols])
    # INSERT
    for row in listOfRows:
        insert_query = db.queryBuilder('INSERT', 'TotalCarbonEmissions', row)
        db.executeQuery(insert_query)

    # Test SELECT
    select_query = db.queryBuilder('SELECT', 'TotalCarbonEmissions')
    db.executeQuery(select_query)

    # Test WHERE
    where_query = db.queryBuilder('WHERE', 'TotalCarbonEmissions', "year='1959'")
    db.executeQuery(where_query)

    # Test UPDATE
    update_query = db.queryBuilder('UPDATE', 'TotalCarbonEmissions', "year='1958' WHERE year='1959'")
    db.executeQuery(update_query)

    # Test DELETE
    delete_query = db.queryBuilder('DELETE', 'TotalCarbonEmissions', "year='1960'")
    db.executeQuery(delete_query)


