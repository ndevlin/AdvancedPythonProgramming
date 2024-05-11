
'''
Nathan Devlin
CSV to JSON
May 10th 2024
'''

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


class TestDataFrames(unittest.TestCase):

    def test_convertToPandasDataFrame(self):

        webScraper = WebScraper()

        webScraper.memberDict = {
            'tr': ['\nheader1\nheader2\n', '\n1\n', '\n2\n'],
            'td': ['\ndata1\n', '\ndata2\n', '\ndata3\n', '\ndata4\n']
        }

        webScraper.convertToPandasDataFrame()

        self.assertEqual(list(webScraper.dataFrame.columns), ['header1', 'header2'])
        self.assertEqual(webScraper.dataFrame.iloc[0, 0].strip(), 'data1')
        self.assertEqual(webScraper.dataFrame.iloc[0, 1].strip(), 'data2')
        self.assertEqual(webScraper.dataFrame.iloc[1, 0].strip(), 'data3')
        self.assertEqual(webScraper.dataFrame.iloc[1, 1].strip(), 'data4')
        
        
def main():
    webScraper = WebScraper()

    webScraper.webPageFromFile("GHGEmissions.html")

    relevantTags = ["th", "tr", "td"]

    for tag in relevantTags:
        tableData = webScraper.extractTags(tag)
        webScraper.cleanTags(tableData)
    
    webScraper.convertToPandasDataFrame()
    webScraper.printDataFrame()
    
    unittest.main()
    

if __name__ == "__main__":
    main()

