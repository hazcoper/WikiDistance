import os
import json
import pickle


fileList = [os.path.join("db", x) for x in os.listdir("db")]
print(fileList)


def getSize():

    referenceCount = 0
    articleCount = 0


    for name in fileList:
        with open(name, "rb") as read_file:
            myDict = pickle.load(read_file)

        articleCount += len(myDict.keys())
        for key in myDict.keys():
            referenceCount += len(myDict[key]["links"])

    print(f"This is the number of articles {articleCount}")
    print(f"This is the average number of links {referenceCount/articleCount} ")


def getDuplicates():
    #lets check for repetition in the list
    counter = 0
    for name in fileList:
        print(name)
        with open(name, "rb") as read_file:
            myDict = pickle.load(read_file)

        for article in myDict:
            myList = myDict[article]["links"]

            emptyDict = {}

            for value in myList:
                if value in emptyDict:
                    emptyDict[value] += 1
                else:
                    emptyDict[value] = 0
            
            if len(myList) != len(emptyDict.keys()):
                print(f"{article} has: {len(myList)} but only {len(emptyDict.keys())} are unique")
                counter += 1
            # print(f"{len(emptyDict.keys())} out of {len(myList)} {len(myList)/len(emptyDict.keys())}")
    print(counter)

getSize()

