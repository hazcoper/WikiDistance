#!/usr/bin/python3

import requests
import time
from Database import MyDatabase

from pprint import pprint

blackist = ["Help:", "Category:", "Talk:", "Wikipedia:", "Template:", "Template talk", "Portal:"]


myDatabase = MyDatabase()
start = time.time()

S = requests.Session()

def tempAdd(wikiData, results):
    """
    Will receive the data raw from wikipedia and will add it to the results list
    """
    results += wikiData["query"]["pages"][list(wikiData["query"]["pages"])[0]]["links"]

def checkBlacklist(word):
    """
    receives a word and checks if its in the blacklist or not
    """
    if word[0] == ".":
        # ignore pages that start with a dot
        return False
    for entry in blackist:
        if entry in word:
            return False
    
    return True

def tempAdd1(wikiData, results):
    if "-1" in wikiData["query"]["pages"]:
        return
    
    tempList = wikiData["query"]["pages"][list(wikiData["query"]["pages"])[0]]["links"]
    results += [x["title"] for x in tempList if checkBlacklist(x["title"])]

def do_request(article):
    """
    Receives article name and returns a list with all the articles that are linked in the given article
    """

    isDone = False
    results = []

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "titles": article,
        "action": "query",
        "format": "json",
        "prop": "links",
        "pllimit": "500",
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    
    tempAdd1(DATA, results)
    isDone = False if "continue" in DATA else True
    counter = 1
    while not isDone:

        PARAMS.update(DATA["continue"])
        
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        # pprint(DATA)

        tempAdd1(DATA, results)
        isDone = False if "continue" in DATA else True
        counter +=1
    print(f"  There was {counter*500} links")
    return results


#I will have two articles, the base article (where I am looking for other articles) and the link article
# the link article is a link in the base article, and will be adding it as a possible base article
# the link article is actually named nextArticle

def main():
    # data = do_request("Pillars of Creation")
    
    #gonna start with portugal, get all the links, get one random article from there and try that

    baseLink = "NASA"
    data = do_request(baseLink)
    myDatabase.appendReferenceList(baseLink, data)
    nextArticle = 0
    counter = 0
    x = 0
    while x < 50:
        print()
        if nextArticle == -1:
            x += 1
            baseLink = myDatabase.getBaseArticle()
            nextArticle = myDatabase.getNextLink(baseLink)
            
            print(f"[CHANGE] - new base link {baseLink}")


        else:
            nextArticle = myDatabase.getNextLink(baseLink)
            if nextArticle == -1:
                print("done with all the articles")
                continue
            print(f"Doing {nextArticle} in {baseLink}")
            data = do_request(nextArticle)
            myDatabase.appendReferenceList(nextArticle, data)
            counter += 1

    # data = do_request("Sérgio Azevedo")

if __name__ == '__main__':
    main()
    myDatabase.saveAndExit()

print(f"Time:{time.time() - start}")