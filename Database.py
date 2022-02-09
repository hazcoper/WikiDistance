import random
import json
import os
import pickle
import threading
import time

"""
articles are stored in dict of their first letter
    each article has three entreis
        list --> links
        int  --> index represents what links of the articles have been seen

in order avoid one big file size (which is harder to manage) I am dividing the database in many files
sorted by the first letter of the articles
and i have implemented a way in which i can specify how many I want to be loaded into memory

change to have one lock per dict and not a global lock
"""


class MyDatabase():

    def __init__(self):
        self.myDict = {}

        self.fileName = None

        self.saveat = 50    #after x articles have been added, should save everything
        self.count = 0

        self.loadedList = {} #dictionary with the letter as key and dictionary with links as value
        self.loadQuant = 10   #how many dicts to be loaded at once in memory
        self.loadedNum = 0


        self.lock = threading.Lock()


    def getName(self, letter):
        """
        Receives a letter and returns the name of the dictionary saved in disk

        used to save and load the dicts
        """

        return os.path.join("db", f"{letter.lower()}.pickle")

    def saveDict(self, letter, name):
        """
        Receives a letter and name that represents a  dict that is loaded in memory and will save said dict to disk
        
        does not need lock because it is an internal function
        """
        
        if letter not in self.loadedList:
            print(f"[saveDict] - dict representing letter {letter} not in memory")
            return False

        #save to the file (overwritting)
        # with open(name, "w") as write_file:
        #     json.dump(self.loadedList[letter], write_file)

        with open(name, "wb") as write_file:
            pickle.dump(self.loadedList[letter], write_file)


    def _saveAll(self):
        """
        Will save all of the dicts that are loaded into memory, but not remove them
        
        does not need lock because it is an internal function and it will already be locked
        """

        for letter in self.loadedList:
            self.saveDict(letter, self.getName(letter))


    def saveAndExit(self):
        """
        Will offload all loaded dicts to disk in order to close the application

        does not require locks because only one thing will run this (because it is to close the application)
            might need to change this
        """
        myList = list(self.loadedList)
        for letter in myList:
            self._removeFromMemory(letter)

    def _removeFromMemory(self, letter):
        """
        Receives a letter and will do the process of removing the dictionary from memory.
        basically save the dictionary

        will not require locking because it is a internal function and it will already be locked
        """

        if letter not in self.loadedList:
            print(f"[removeFromMemory] - dict representing letter {letter} not in memory")
            return False

        #lets save the dict, i need the name before
        name = self.getName(letter)
        self.saveDict(letter, name)

        # this is the dictionary that I want to unload
        myDict = self.loadedList.pop(letter)


        self.loadedNum -= 1
    
    def _loadToMemory(self, letter):
        """
        Receives a letter and will load the given dictionary to memory
        will remove random element from the list
        
        will not require locking because it is an internal function and it will already be locked once it reaches here
        """
        if letter in self.loadedList:
            print(f"[loadToMemory] - dict representing letter {letter} is already in memory")
            return False


        #need to check that I have space in memory
        if self.loadedNum >= self.loadQuant:
            self._removeFromMemory(random.choice(list(self.loadedList)))


        name = self.getName(letter)

        #check if dictionary already exists or not
        if os.path.split(name)[-1] not in os.listdir("db"):
            
            self.loadedList[letter] = {}
            # print("Created with this name ", name)
        else:
            # with open(name, "r") as read_file:
            #     self.loadedList[letter] = json.load(read_file)

            with open(name, "rb") as read_file:
                self.loadedList[letter] = pickle.load(read_file)

        self.loadedNum += 1

    def getNextLink(self, article):
        """
        Will return the next link from the article that has not been seen yet.
        will return None if article does not exist
        will return -1 when all the links have been seen
        """

        self.lock.acquire()
        #have to check if dict is loaded in memory
        if article[0] not in self.loadedList:
            #means that the dict is not loaded in memory and I want to load it
            self._loadToMemory(article[0])

        #check if article has been indexed or not
        print("This is the keys: ", list(self.loadedList))
        # print(f"{article} keys {list(self.loadedList[article[0]])}")
        if len(list(self.loadedList[article[0]])) == 0:
            print(self.loadedList[article[0]])
        if article not in self.loadedList[article[0]]:
            print(f"[getNextLink] - article {article} has not been indexed yet")
            self.lock.release()

            return False


        index = self.loadedList[article[0]][article]["index"]
        if index == len(self.loadedList[article[0]][article]["links"]):
            self.lock.release()

            return -1
        link = self.loadedList[article[0]][article]["links"][index]
        self.loadedList[article[0]][article]["index"] += 1

        self.lock.release()
        return link

    def getLinks(self, article):
        """
        Will return a set with all of the links in a certain article
        """

        self.lock.acquire()
        #have to check if dict is loaded in memory
        if article[0] not in self.loadedList:
            #means that the dict is not loaded in memory and I want to load it
            self._loadToMemory(article[0])


        returnValue = self.loadedList[article[0]][article]["links"]
        self.lock.release()
        return returnValue

    def markArticle(self, article):
        """
        Will mark an article to represent that it has already been seen
        meaning that it all the links inside have been looked at
        """
        self.lock.acquire()
        #have to check if dict is loaded in memory
        if article[0] not in self.loadedList:
            #means that the dict is not loaded in memory and I want to load it
            self._loadToMemory(article[0])

        self.loadedList[article[0]][article]["index"] = 1
        self.lock.release()

    def _fillMemoryRandom(self):
        """
        Will fill the memory with random letters

        does not need locking because it is an internal funtion
        """

        letterList = [x.split(".")[0] for x in os.listdir("db")]
        while self.loadedNum < self.loadQuant:
            self._loadToMemory(random.choice(letterList))

    def getBaseArticle(self):
        """
        Will return an article where not all the links have been seen yet
        Will only return from the a dictionary that is loaded
            will need to deal with what happens when all of the articles that are loaded have been seen
        
        will need to change this, because there might be articles that have not been seen yet in dicts that are not loaded in memory
        """
        self.lock.acquire()
        #iterate over all the loaded dicts
        #   look for an article that has the index < len of the list
        #   return that value

        #check to see if there is any loaded letter
        if self.loadedNum == 0:
            self._fillMemoryRandom()

        for letter in self.loadedList:
            print(f"        THis is the letter {letter}")
            for article in self.loadedList[letter]:
                myLen = len(self.loadedList[letter][article]["links"])
                myIndex = self.loadedList[letter][article]["index"]
                print(f"           THis is the article {article}, len {myLen}, index {myIndex}")
                if self.loadedList[letter][article]["index"] == 0:
                    self.loadedList[letter][article]["index"] = -1   #indicate that it is being seen

                    self.lock.release()
                    return article
    
        self.lock.release()
        print("here returned false!")
        print("[getBaseArticle] - PROBLEM - all articles have been fully seen, this should not happen")

        return False

    def getDictSize(self):
        print("Please implement me")

    def addSingleEntry(self, key, singleValue): 
        print(" please implement me")

    def isEmpty(self):
        """
        Returns true if the database is empty
        returns false if the databse is not empty

        just because files exists does not mean that the database is not empty, need to check this
        """

        if len(os.listdir("db")) == 0:
            return True #yes the dict is empty
        
        #no the dict is not empty
        return False


    def appendReferenceList(self, article, valueList):
        """"
        Receives a article name representing a wikipedia page and a value representing a list of links present in said article
        and will add it to the databse
        """
        self.lock.acquire()
        self.count += 1

        if self.count % self.saveat == 0:
            print(f"[SAVED] --> count is {self.count}")
            self._saveAll()

        #check if I need to load the dictionary to memory
        # print(f"this is the article {article}")
        if article[0] not in self.loadedList:
            self._loadToMemory(article[0])

        #i should check if the list that I am adding, if elements are not already in the list
        #maybe use a set?
        
        if article in self.loadedList[article[0]]:
            self.loadedList[article[0]][article]["links"].update(valueList)
            self.loadedList[article[0]][article]["index"] = 0 #each time i add a new article, I want to make sure that I update de index value

        else:
            self.loadedList[article[0]][article] = {}
            self.loadedList[article[0]][article]["links"] = set()
            self.loadedList[article[0]][article]["links"].update(valueList)

            self.loadedList[article[0]][article]["index"] = 0

        self.lock.release()


    def getRandomLink(self, article):
        """
        Will return random link inside that article
        will return None if article does not exist
        """
        print("Please impelent me")        

    def hasArticle(self, article):
        """
        Will receive and article and check to see if the article already exists in the dabase or not
        it will also check if the article has already been processed or not

        and article that has been processed, is an article that I have seen all of the links.
        
        return 0 == not present
        return 1 == present but not seen
        return 2 == present and seen
        """

        self.lock.acquire()
        #have to check if dict is loaded in memory
        if article[0] not in self.loadedList:
            #means that the dict is not loaded in memory and I want to load it
            self._loadToMemory(article[0])

        if article in self.loadedList[article[0]]:
            #means that the article is present
            if self.loadedList[article[0]][article]["index"] == 1:
                #means that it has been seen already
                self.lock.release()

                return 2
            self.lock.release()

            return 1
        self.lock.release()
        return 0

    def removeEntry(self):
        print("Please implement me")







if __name__ == '__main__':

    db = MyDatabase()


    print(db.hasArticle("Baixo Alentejo Province"))
    db.saveAndExit()
