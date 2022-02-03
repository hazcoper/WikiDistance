import random
import json
import os

"""
articles are stored in dict of their first letter
    each article has three entreis
        list --> links
        int  --> index represents what links of the articles have been seen

in order avoid one big file size (which is harder to manage) I am dividing the database in many files
sorted by the first letter of the articles
and i have implemented a way in which i can specify how many I want to be loaded into memory


"""


class MyDatabase():

    def __init__(self):
        self.myDict = {}

        self.fileName = None

        self.saveat = 10 #entries

        self.loadedList = {} #dictionary with the letter as key and dictionary with links as value
        self.loadquant = 10   #how many dicts to be loaded at once in memory
        self.loadedNum = 0


    def getName(self, letter):
        """
        Receives a letter and returns the name of the dictionary saved in disk
        """
        return os.path.join("db", f"{letter.lower()}.json")

    def saveAndExit(self):
        """
        Will offload all loaded dicts to disk in order to close the application
        """
        myList = list(self.loadedList)
        for letter in myList:
            self.removeFromMemory(letter)

    def removeFromMemory(self, letter):
        """
        Receives a letter and will do the process of removing the dictionary from memory.
        basically save the dictionary
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
        
    
    def loadToMemory(self, letter):
        """
        Receives a letter and will load the given dictionary to memory
        will remove random element from the list
        """

        if letter in self.loadedList:
            print(f"[loadToMemory] - dict representing letter {letter} is already in memory")
            return False


        #need to check that I have space in memory
        if self.loadedNum >= self.loadquant:
            self.removeFromMemory(random.choice(list(self.loadedList)))


        name = self.getName(letter)

        #check if dictionary already exists or not
        if os.path.split(name)[-1] not in os.listdir("db"):
            print(os.listdir("db"), name)
            self.loadedList[letter] = {}
            print("Created with this name ", name)
        else:
            with open(name, "r") as read_file:
                self.loadedList[letter] = json.load(read_file)

        self.loadedNum += 1

    def getNextLink(self, article):
        """
        Will return the next link from the article that has not been seen yet.
        will return None if article does not exist
        will return -1 when all the links have been seen
        """

        #have to check if dict is loaded in memory
        if article[0] not in self.loadedList:
            #means that the dict is not loaded in memory and I want to load it
            self.loadToMemory(article[0])

        #check if article has been indexed or not
        print("This is the keys: ", list(self.loadedList))
        # print(f"{article} keys {list(self.loadedList[article[0]])}")
        if len(list(self.loadedList[article[0]])) == 0:
            print(self.loadedList[article[0]])
        if article not in self.loadedList[article[0]]:
            print(f"[getNextLink] - article {article} has not been indexed yet")
            return False


        index = self.loadedList[article[0]][article]["index"]
        if index == len(self.loadedList[article[0]][article]["links"]):
            return -1
        link = self.loadedList[article[0]][article]["links"][index]
        self.loadedList[article[0]][article]["index"] += 1

        return link

    def getBaseArticle(self):
        """
        Will return an article where not all the links have been seen yet
        Will only return from the a dictionary that is loaded
            will need to deal with what happens when all of the articles that are loaded have been seen
        """

        #iterate over all the loaded dicts
        #   look for an article that has the index < len of the list
        #   return that value
        for letter in self.loadedList:
            print(f"        THis is the letter {letter}")
            for article in self.loadedList[letter]:
                myLen = len(self.loadedList[letter][article]["links"])
                myIndex = self.loadedList[letter][article]["index"]
                print(f"           THis is the article {article}, len {myLen}, index {myIndex}")
                if len(self.loadedList[letter][article]["links"]) > self.loadedList[letter][article]["index"]:
                    return article

        print("[getBaseArticle] - PROBLEM - all articles have been fully seen, this should not happen")

    def getDictSize(self):
        print("Please implement me")

    def addSingleEntry(self, key, singleValue): 
        print(" please implement me")

    def appendReferenceList(self, article, valueList):
        """"
        Receives a article name representing a wikipedia page and a value representing a list of links present in said article
        and will add it to the databse
        """

        #check if I need to load the dictionary to memory
        # print(f"this is the article {article}")
        if article[0] not in self.loadedList:
            self.loadToMemory(article[0])
        
        #i should check if the list that I am adding, if elements are not already in the list
        #maybe use a set?
        
        if article in self.loadedList[article[0]]:
            self.loadedList[article[0]][article]["links"] += valueList
        else:
            self.loadedList[article[0]][article] = {}
            self.loadedList[article[0]][article]["links"] = valueList
            self.loadedList[article[0]][article]["index"] = 0

    def getRandomLink(self, article):
        """
        Will return random link inside that article
        will return None if article does not exist
        """
        print("Please impelent me")        

    def removeEntry(self):
        print("Please implement me")


    def saveDict(self, letter, name):
        """
        Receives a letter and name that represents a  dict that is loaded in memory and will save said dict to disk
        """
        
        if letter not in self.loadedList:
            print(f"[saveDict] - dict representing letter {letter} not in memory")
            return False
        #save to the file (overwritting)
        with open(name, "w") as write_file:
            json.dump(self.loadedList[letter], write_file)


    # def loadDict(self):        
    #     """
    #     need to implement more security, search for a specific file
    #     add a signature to the file
    #     add a way to compare the dictionary that is being loaded with the one already present
    #     """
    #     #check if there is a file already

    #     if self.fileName == None:
    #         self.fileName = self.searchDir()
    #         if self.fileName == None:
    #             #means that there is no save file
    #             print("No file has been found")
    #             return
         
    #     with open(self.fileName, "r") as read_file:
    #         self.myDict = json.load(read_file)

    #     print("json has been loaded")

    # def searchDir(self):
    #     """
    #     Will search the root directory for the dictionary
        

    #     Returns the path to the dictionary. if there is no dictionary present it returns none 
    #     """
    #     jsonList = [x for x in os.listdir() if x.split(".")[-1] == "json"]
    #     if len(jsonList) > 0:
    #         return jsonList[0]
    #     else:
    #         return None



if __name__ == '__main__':

    db = MyDatabase()
    main()
    myDatabase.saveDict()


