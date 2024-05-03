'''
Rotating Caesar Cypher encryption and decryption
Mid 1 Q


class Decryption:

    def __init__(self, shift):
        self.shift = shift

    def caesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal + shift
            if newAsciiVal > 0x80:
                newAsciiVal = newAsciiVal - 0x80 + 0x20 - 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString

    def decryptCaesarCypher(self, inputString):
        outputString = ""
        shift = self.shift
        for char in inputString:
            asciiVal = ord(char)
            newAsciiVal = asciiVal - shift
            if newAsciiVal < 0x20:
                newAsciiVal = newAsciiVal + 0x80 - 0x20 + 1
            outputString += chr(newAsciiVal)
            shift += 1
        return outputString


# Main

stringToEncrypt = "HELLO"

decrypter = Decryption(shift=5)

print("Encrypt", stringToEncrypt)
encryptedString = decrypter.caesarCypher(stringToEncrypt)
print(encryptedString)

print("Decrypt ", encryptedString)
decryptedString = decrypter.decryptCaesarCypher(encryptedString)
print(decryptedString)



import sqlite3
import unittest

class SqliteManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

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


class TestDecryption(unittest.TestCase):

    def testEncryptionDecryption(self):

        databaseName = "Mid1.db"

        with SqliteManager(databaseName) as db:

            tableTupleData = "(Text1 TEXT, Text2 TEXT)"

            # CREATE TABLE
            createTableQuery = db.queryBuilder('CREATE TABLE', 'TextTable', tableTupleData)
            db.executeQuery(createTableQuery)

            textToInsert = ("Hello", "World")
            insertQuery = db.queryBuilder('INSERT', 'TextTable', textToInsert)
            db.executeQuery(insertQuery)

            print(f"{insertQuery = }")
            print()

            decrypter = Decryption(shift=3)
            originalString = insertQuery
            print(f"{originalString = }")
            encryptedString = decrypter.caesarCypher(originalString)
            print(f"{encryptedString = }")
            decryptedString = decrypter.decryptCaesarCypher(encryptedString)
            print(f"{decryptedString = }")
            self.assertEqual(originalString, decryptedString)
            print("originalString == decryptedString?" , originalString == decryptedString)


if __name__ == '__main__':
    unittest.main()
'''


# From Dataframes
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

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

    def extractTags(self, tagIn):
        if self.soup == None:
            print("Webpage was not loaded")
            return
        
        tagResult = None
        tagResult = self.soup.select(tagIn)
        if tagResult == None:
            print("No tags were found")
            return

        output = []

        for i in range(0, len(tagResult)):
            output.append(str((tagResult)[i].text))

        return (tagIn, tuple(output))

    def cleanTags(self, tagTupleIn):
        self.memberDict[tagTupleIn[0]] = tagTupleIn[1]

    def getData(self):
        return self.memberDict.items()

    def convertToPandasDataFrame(self):
        if self.memberDict == defaultdict(list):
            print("Must Clean Tags before converting to Pandas DataFrame")
            return
        
        try:
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
        except:
            print("Conversion to DataFrame failed")
        
        return self.dataFrame
    
    def printDataFrame(self):
        print(self.dataFrame)

        
# DataFrames Code
webScraper = WebScraper()

webScraper.webPageFromFile("GHGEmissions.html")

relevantTags = ["th", "tr", "td"]

for tag in relevantTags:
    tableData = webScraper.extractTags(tag)
    webScraper.cleanTags(tableData)

originalDataFrame = webScraper.convertToPandasDataFrame()

print(originalDataFrame)

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

print(averageEmissionsDataFrame)





# 

import tkinter as tk
from tkinter import ttk

'''
TKinter GUI to display the DataFrame
'''
def display_dataframe(df):
    window = tk.Tk()
    window.title("DataFrame Display")

    notebook = ttk.Notebook(window)

    tab1 = ttk.Frame(notebook)

    notebook.add(tab1, text='Average Agriculture Emissions by Country')

    notebook.pack()

    def create_table(tab, rows, cols):
        for r in range(rows):
            for c in range(cols):
                if r == 0: # Headers
                    cell = ttk.Label(tab, text=df.columns[c], wraplength=200)
                else:
                    cellText = df.iloc[r, c]   
                    cell = ttk.Label(tab, text=cellText)
                cell.grid(row=r, column=c)

    create_table(tab1, df.shape[0], df.shape[1])  # DataFrame

    window.mainloop()

# Main Code
display_dataframe(averageEmissionsDataFrame)




