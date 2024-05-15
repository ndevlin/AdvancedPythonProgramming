
'''
Nathan Devlin
CSV to JSON
May 10th 2024
'''

from collections import defaultdict
from io import StringIO
import re
import unittest
import numpy as np
import pandas as pd
import csv
import tkinter as tk
from tkinter import ttk

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


class TestWebScraper(unittest.TestCase):
    def setUp(self):
        self.webScraper = WebScraper()

    def test_parseCSVtoDict_convertToPandasDataFrame(self):
        self.webScraper.parseCSVtoDict("Dwarfs.csv")
        self.webScraper.convertToPandasDataFrame()
        jsonCSV = self.webScraper.getDataFrame().to_json()
        expected_output = (
            '{"Dwarf":{"0":"Ceres","1":"Pluto","2":"Haumea","3":"Makemake","4":"Eris",'
            '"5":"Orcus","6":"2003AZ84","7":"Ixion","8":"90568","9":"55636","10":"Quaoar",'
            '"11":"55565","12":"Sedna"},"Distance(AU)":{"0":"2.77","1":"39.5","2":"43.19",'
            '"3":"45.48","4":"67.84","5":"39.22","6":"39.36","7":"39.70","8":"42.10",'
            '"9":"43.28","10":"43.12","11":"47.12","12":"488.98"},"Period(years)":'
            '{"0":"980","1":"2370","2":"283.84","3":"306.17","4":"558.77","5":"246.94",'
            '"6":"246.94","7":"250.18","8":"2273.13","9":"284.69","10":"287.97",'
            '"11":"323.49","12":"10812.82"}}'
        )        
        self.assertEqual(jsonCSV, expected_output)

# Main
def main():    
    webScraper = WebScraper()

    webScraper.parseCSVtoDict("Dwarfs.csv")

    print(f"{webScraper.getData() = }", "\n")

    webScraper.convertToPandasDataFrame()

    print("webScraper.dataFrame:")
    webScraper.printDataFrame()

    print()

    jsonCSV = webScraper.getDataFrame().to_json()

    print(f"{jsonCSV = }", "\n")

    backToDataFrame = pd.read_json(StringIO(jsonCSV))

    print(backToDataFrame, "\n")

    unittest.main()


if __name__ == '__main__':
    main()

