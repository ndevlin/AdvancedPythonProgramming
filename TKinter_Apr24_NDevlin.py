'''
Nathan Devlin
TKinter
April 24th
'''

from collections import defaultdict
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk

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
    
    def printDataFrame(self):
        print(self.dataFrame)


def display_dataframe(df):
    root = tk.Tk()
    root.title("DataFrame Display")

    # Create the tab control
    tab_control = ttk.Notebook(root)

    # Create the tabs
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    # Add the tabs to the tab control
    tab_control.add(tab1, text='DataFrame')
    tab_control.add(tab2, text='Headers')
    tab_control.add(tab3, text='Indices')

    # Pack the tab control
    tab_control.pack(expand=1, fill='both')

    # Function to create a table in a tab
    def create_table(tab, rows, cols):
        for r in range(rows):
            for c in range(cols):
                cell = ttk.Label(tab, text=df.iat[r, c] if r < df.shape[0] and c < df.shape[1] else "")
                cell.grid(row=r, column=c)

    # Create the tables
    create_table(tab1, df.shape[0], df.shape[1])  # DataFrame
    create_table(tab2, 1, df.shape[1])  # Headers
    create_table(tab3, df.shape[0], 1)  # Indices

    root.mainloop()

# Test the function
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

webScraper = WebScraper()

webScraper.webPageFromFile("GHGEmissionsTestVersion.html")

relevantTags = ["th", "tr", "td"]

for tag in relevantTags:
    tableData = webScraper.extractTags(tag)
    webScraper.cleanTags(tableData)

webScraper.convertToPandasDataFrame()
webScraper.printDataFrame()

df = webScraper.dataFrame

display_dataframe(df)

