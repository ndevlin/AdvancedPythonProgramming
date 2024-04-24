'''
Nathan Devlin
Data Aqcuisition
Apr 12 2024
'''

import re
from collections import defaultdict
import unittest


def convertHtmlToString(fileName):
    with open(fileName, "r") as file:
        return file.read()


def extractTags(htmlIn, tagIn):
    """
    Note that tagIn is assumed to be a string taking the form of just the text 
    portion of the tag, e.g. "tr", not "<tr>"
    """

    openPattern = r"<.*" + tagIn + r".*>"
    closePattern = r"</.*" + tagIn + r".*>"
    
    lines = htmlIn.splitlines()
    strippedLines = []
    for i in range(len(lines)):
        strippedLines.append(lines[i].strip())

    output = []
    outputString = ""
    appendString = False
    for line in strippedLines:
        if re.match(openPattern, line):
            appendString = True

        if appendString == True:
            outputString += line
            if re.search(closePattern, line):
                appendString = False
                output.append(outputString)
                outputString = ""
            else:
                outputString += "\n"

    return (tagIn, tuple(output))

def cleanTags(tagTupleIn):
    outputDict = defaultdict(None)
    outputDict[tagTupleIn[0]] = tagTupleIn[1]
    return outputDict


class TestScraping(unittest.TestCase):

    testText = ""
    testTuple = ()

    def setUp(self):
        self.testText = convertHtmlToString("Dwarfplanets.html")

    def test_ExtractTag_table(self):
        testResult = extractTags(self.testText, "table")

        expectedResult = ('table', ("""<table class = dwarfs>
<tr>\n<th>Dwarf</th>\n<th>Distance(AU)</th>\n<th>Period</th>\n</tr>\n<tr>\n<td>Pluto</td>\n<td>39.5</td>\n<td>247.69</td>
</tr>\n<tr>\n<td>Eris</td>\n<td>67.84</td>\n<td>558.77</td>\n</tr>\n<tr>\n<td>Haumea</td>\n<td>43.19</td>\n<td>283.84</td>
</tr>\n<tr>\n<td>Makemake</td>\n<td>45.48</td>\n<td>306.17</td>\n</tr>\n<tr>\n<td>Ceres</td>\n<td>2.77</td>\n<td>4.61</td>
</tr>\n</table>""",))
        self.assertEqual(testResult, expectedResult)



    def test_ExtractTag_tr(self):
        testResult = extractTags(self.testText, "tr")

        expectedResult = ('tr', ('<tr>\n<th>Dwarf</th>\n<th>Distance(AU)</th>\n<th>Period</th>\n</tr>',\
                                 '<tr>\n<td>Pluto</td>\n<td>39.5</td>\n<td>247.69</td>\n</tr>', \
                                    '<tr>\n<td>Eris</td>\n<td>67.84</td>\n<td>558.77</td>\n</tr>', \
                                        '<tr>\n<td>Haumea</td>\n<td>43.19</td>\n<td>283.84</td>\n</tr>', \
                                            '<tr>\n<td>Makemake</td>\n<td>45.48</td>\n<td>306.17</td>\n</tr>', \
                                                '<tr>\n<td>Ceres</td>\n<td>2.77</td>\n<td>4.61</td>\n</tr>'))

        self.assertEqual(testResult, expectedResult)


    def test_cleanTags_tr(self):
        testResult = cleanTags(extractTags(self.testText, "tr"))
        self.assertEqual(testResult, defaultdict(None, {'tr': ('<tr>\n<th>Dwarf</th>\n<th>Distance(AU)</th>\n<th>Period</th>\n</tr>', \
                                                               '<tr>\n<td>Pluto</td>\n<td>39.5</td>\n<td>247.69</td>\n</tr>', \
                                                                '<tr>\n<td>Eris</td>\n<td>67.84</td>\n<td>558.77</td>\n</tr>', \
                                                                    '<tr>\n<td>Haumea</td>\n<td>43.19</td>\n<td>283.84</td>\n</tr>', \
                                                                        '<tr>\n<td>Makemake</td>\n<td>45.48</td>\n<td>306.17</td>\n</tr>', \
                                                                            '<tr>\n<td>Ceres</td>\n<td>2.77</td>\n<td>4.61</td>\n</tr>')}))


def main():
    
    dwarfPlanetsContents = convertHtmlToString("Dwarfplanets.html")

    relevantTags = [""]
    output = extractTags(dwarfPlanetsContents, "tr")

    print(output)

    print(cleanTags(output))

    unittest.main()


if __name__ == "__main__":
    main()

