'''
Nathan Devlin
Classes
Apr 15 2024
'''

from collections import defaultdict

from urllib.request import urlopen

from bs4 import BeautifulSoup


class WebScraper():

    def __init__(self):
        self.soup = None
        self.memberDict = defaultdict(list)

    def requestWebPage(self, pageIn):
        try:
            html = urlopen(pageIn)
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
    

def main():
    
    '''
    Test WebScraper class with refactored WebScraping code:
    '''

    webScraper = WebScraper()

    webScraper.requestWebPage("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita")

    relevantTags = ["table", "th", "tr", "td"]

    for tag in relevantTags:
        tableData = webScraper.extractTags(tag)
        webScraper.cleanTags(tableData)

    for key, value in webScraper.getData():
        print(key, ":", value)
        import time
        time.sleep(2)
        print()
        print()


if __name__ == "__main__":
    main()

