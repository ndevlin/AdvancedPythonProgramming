
'''
Nathan Devlin
TKinter
April 24th
'''

from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup

import os
import re
import unittest

import numpy as np

import pandas as pd

import DataFrames_Apr23_NDevlin as dataFrames
        
        
def main():
    webScraper = dataFrames.WebScraper()

    webScraper.webPageFromFile("GHGEmissionsTestVersion.html")

    relevantTags = ["th", "tr", "td"]

    for tag in relevantTags:
        tableData = webScraper.extractTags(tag)
        webScraper.cleanTags(tableData)
    
    webScraper.convertToPandasDataFrame()
    webScraper.printDataFrame()
    
    unittest.main()
    

if __name__ == "__main__":
    main()

