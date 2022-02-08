#!/usr/bin/python3

import requests
import time
from Database import MyDatabase
import threading

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
    # print(f"  There was {counter*500} links in {article}")
    return results, counter*500


#I will have two articles, the base article (where I am looking for other articles) and the link article
# the link article is a link in the base article, and will be adding it as a possible base article
# the link article is actually named nextArticle

def work(name):

    #get a baseLink
    myLink = myDatabase.getBaseArticle()
    #get the data
    data,c = do_request(myLink)
    #save the data
    myDatabase.appendReferenceList(myLink, data)

    #get the link of the links
    linkList = myDatabase.getLinks(myLink)
    
    for link in linkList:
        data,c = do_request(link)
        myDatabase.appendReferenceList(link, data)
    print(f"[THREAD-{name}] --> did {myLink} --> {c}")



def main():
    # data = do_request("Pillars of Creation")
    
    #gonna start with portugal, get all the links, get one random article from there and try that




# i give a base article
# the program will check if the base article already exists in the database or not
#     if it is already in the database, it will check if it has been seen yet
#         if it has been seen, than it will pick another base article
    
#         if it has not been seen yet, it will get all the links of the links

#     if it is not in the database, it will get the links and add it to the databse

    #para x baseLinks
    #   vou pegar no em todos os links que estao no baseLink
    #      vou pegar em todos os links que estao nos links do baseLink
    #

    #get the first article
    baseLink = "Rubicon"
    data, c = do_request(baseLink)
    myDatabase.appendReferenceList(baseLink, data)
    
    #get the link of the links
    mySet = myDatabase.getLinks(baseLink)
    
    for link in mySet:
        data,c = do_request(link)
        myDatabase.appendReferenceList(link, data)

    print(f"[THREAD-MAIN] --> did {baseLink} --> {c}")

    # lets create the thread
    counter = 0
    for i in range(4):
        t = threading.Thread(target=work, args=(counter,))
        t.start()
        counter += 1


    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()



    # baseLink = "Rubicon"
    # for x in range(2): #get 10 base articles
    #     print(f"\nDoing {baseLink}")
    #     hasArticle = myDatabase.hasArticle(baseLink) 
    #     if hasArticle == 2: #means that the article exists and that I have already seen it
    #         print("it has been seen already")
    #         baseLink = myDatabase.getBaseArticle()
    #         continue

    #     if hasArticle == 1: #means that the article exists but it has not been seen yet
    #         #i want to get and get the link at everysingle of this entries
    #         print("it has not been seen yet")
    #         mySet = myDatabase.getLinks(baseLink)
            
    #         for link in mySet:
    #             data = do_request(link)
    #             myDatabase.appendReferenceList(link, data)
            
    #         myDatabase.markArticle(baseLink);
    #         baseLink = myDatabase.getBaseArticle()
    #         continue

    #     #i want to get the links in the base link
    #     print("it is not in the database yet")
    #     data = do_request(baseLink)
    #     myDatabase.appendReferenceList(baseLink, data)


        

        # lets check if the article already exists in the database



    # baseLink = "NASA"
    # data = do_request(baseLink)
    # myDatabase.appendReferenceList(baseLink, data)
    # nextArticle = 0
    # counter = 0
    # x = 0
    # while x < 50:
    #     print()
    #     if nextArticle == -1:
    #         x += 1
    #         baseLink = myDatabase.getBaseArticle()
    #         nextArticle = myDatabase.getNextLink(baseLink)
            
    #         print(f"[CHANGE] - new base link {baseLink}")


    #     else:
    #         nextArticle = myDatabase.getNextLink(baseLink)
    #         if nextArticle == -1:
    #             print("done with all the articles")
    #             continue
    #         print(f"Doing {nextArticle} in {baseLink}")
    #         data = do_request(nextArticle)
    #         myDatabase.appendReferenceList(nextArticle, data)
    #         counter += 1

    # data = do_request("Sérgio Azevedo")

if __name__ == '__main__':
    main()
    myDatabase.saveAndExit()

print(f"Time:{time.time() - start}")

