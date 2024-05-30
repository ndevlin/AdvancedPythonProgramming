'''
MatplotLib
May 29 2024
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
        
        headers = self.memberDict["tr"][0]

        #numRows = int(re.search(r'\n(\d+)\n', self.memberDict["tr"][-1]).group(1))
        #numRows = len(self.memberDict["tr"]) - 1
        numRows = 340

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



import tkinter as tk
from tkinter import ttk

'''
TKinter GUI to display the DataFrame
'''
def display_dataframe(df, title):
    window = tk.Tk()
    window.title("DataFrame Display")

    notebook = ttk.Notebook(window)

    tab1 = ttk.Frame(notebook)

    notebook.add(tab1, text=title)

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
title = "Average Agriculture Emissions by Country"
print(title)
print(averageEmissionsDataFrame)
#display_dataframe(averageEmissionsDataFrame, title)



"""
Matplotlib Plotting
"""

import matplotlib.pyplot as plt

class PlotManager:
    def __init__(self, df):
        self.df = df

    def __str__(self):
        return f'PlotManager for DataFrame with {self.df.shape[0]} rows and {self.df.shape[1]} columns'

    def linePlot(self, x=None, y=None, title="Line Plot", xlabel="X-axis", ylabel="Y-axis"):
        if not x or not y:
            x, y = self.df.columns[:2]
        plt.figure()
        plt.plot(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def barPlot(self, x=None, y=None, title="Bar Plot", xlabel="X-axis", ylabel="Y-axis"):
        if not x or not y:
            x, y = self.df.columns[:2]
        plt.figure()
        plt.bar(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def scatterPlot(self, x=None, y=None, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis"):
        if not x or not y:
            x, y = self.df.columns[:2]
        plt.figure()
        plt.scatter(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

# Main Code
plotManager = PlotManager(averageEmissionsDataFrame)
print(plotManager)
plotManager.barPlot(title='Bar Plot Example')

print("Done")

