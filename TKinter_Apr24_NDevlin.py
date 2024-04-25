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

'''
WebScraper class to extract data from a webpage and convert it to a Pandas DataFrame
'''
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


'''
TKinter GUI to display the DataFrame
'''
def display_dataframe(df):
    window = tk.Tk()
    window.title("DataFrame Display")

    notebook = ttk.Notebook(window)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text='DataFrame')
    notebook.add(tab2, text='Headers')
    notebook.add(tab3, text='Indices')

    notebook.pack()

    def create_table(tab, rows, cols):
        for r in range(rows):
            for c in range(cols):
                if r == 0: # Headers
                    cell = ttk.Label(tab, text=df.columns[c], wraplength=150)
                else:
                    cellText = df.iloc[r, c]   
                    cell = ttk.Label(tab, text=cellText)
                cell.grid(row=r, column=c)

    create_table(tab1, df.shape[0], df.shape[1])  # DataFrame
    create_table(tab2, 1, df.shape[1])  # Headers
    create_table(tab3, df.shape[0], 1)  # Indices

    window.mainloop()


'''
Main Code
'''
webScraper = WebScraper()

webScraper.webPageFromFile("GHGEmissionsTestVersion.html")

relevantTags = ["th", "tr", "td"]

for tag in relevantTags:
    tableData = webScraper.extractTags(tag)
    webScraper.cleanTags(tableData)

webScraper.convertToPandasDataFrame()

df = webScraper.dataFrame

display_dataframe(df)

