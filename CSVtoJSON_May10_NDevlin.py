
'''
Nathan Devlin
CSV to JSON
May 10th 2024
'''

from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
import unittest

import numpy as np

import pandas as pd

import csv

class WebScraper():

    def __init__(self):
        self.memberDict = defaultdict(list)
        self.dataFrame = None

    def parseCSVtoDict(self, csvFileName):
        try:
            with open(csvFileName, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # get the headers
                if headers:
                    for row in reader:
                        for header, value in zip(headers, row):
                            if header not in self.memberDict:
                                self.memberDict[header] = []
                            self.memberDict[header].append(value)
        except Exception as e:
            print(f"Issue parsing CSV file: {e}")
    
    def convertToPandasDataFrame(self):
        try:
            self.dataFrame = pd.DataFrame.from_dict(self.memberDict)
        except Exception as e:
            print(f"Issue converting dictionary to DataFrame: {e}")
    
    def printDataFrame(self):
        print(self.dataFrame)

    def getDataFrame(self):
        return self.dataFrame

    def getData(self):
        return self.memberDict.items()


webScraper = WebScraper()

webScraper.parseCSVtoDict("Dwarfs.csv")

print(webScraper.getData())

webScraper.convertToPandasDataFrame()
webScraper.printDataFrame()

jsonCSV = webScraper.getDataFrame().to_json()

print(jsonCSV)
        
