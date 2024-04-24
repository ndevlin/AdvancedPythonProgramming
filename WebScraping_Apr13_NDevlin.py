'''
Nathan Devlin
Web Scraping
Apr 13 2024
'''

import re
from collections import defaultdict
import unittest

from urllib.request import urlopen

from bs4 import BeautifulSoup

def convertHtmlToSoup(pageIn):
    html = urlopen(pageIn)
    return BeautifulSoup(html, "html.parser")


def extractTags(soupIn, tagIn):
    tagResult = soupIn.select(tagIn)
    output = []

    for i in range(0, len(tagResult)):
        output.append(str((tagResult)[i].text))

    return (tagIn, tuple(output))


def cleanTags(tagTupleIn, dictIn = defaultdict(None)):
    outputDict = dictIn
    outputDict[tagTupleIn[0]] = tagTupleIn[1]
    return outputDict


def main():
    
    soup = convertHtmlToSoup("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita")

    relevantTags = ["table", "th", "tr", "td"]

    tagDict = defaultdict(None)

    for tag in relevantTags:
        tableData = extractTags(soup, tag)
        tagDict = cleanTags(tableData, tagDict)

    for key, value in tagDict.items():
        print(key, ":", value)
        print()
        print()


if __name__ == "__main__":
    main()

