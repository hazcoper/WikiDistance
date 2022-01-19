import json
import os

class MyDatabase():

    def __init__(self):
        self.myDict = {}

        self.fileName = None

        self.loadDict()

    # def __del__(self):
    #     if(input("Should I save? ") == "y"):
    #         self.saveDict()

    def saveDict(self):
        """
        Will save the dictionary
        """
        if self.fileName == None:
            self.fileName = self.searchDir()
            if self.fileName == None:
                self.fileName = "myDict.json" #setting new file name

        #save to the file (overwritting)
        with open(self.fileName, "w") as write_file:
            json.dump(self.myDict, write_file)


    def loadDict(self):        
        """
        need to implement more security, search for a specific file
        add a signature to the file
        add a way to compare the dictionary that is being loaded with the one already present
        """
        #check if there is a file already

        if self.fileName == None:
            self.fileName = self.searchDir()
            if self.fileName == None:
                #means that there is no save file
                print("No file has been found")
                return
         
        with open(self.fileName, "r") as read_file:
            self.myDict = json.load(read_file)

        print("json has been loaded")

    def searchDir(self):
        """
        Will search the root directory for the dictionary
        

        Returns the path to the dictionary. if there is no dictionary present it returns none 
        """
        jsonList = [x for x in os.listdir() if x.split(".")[-1] == "json"]
        if len(jsonList) > 0:
            return jsonList[0]
        else:
            return None

    def getDictSize(self):
        print("Please implement me")

    def addEntry(self, key, value):
        """"
        Receives a key representing a wikipedia page and a value representing a link in that page
        will add that said key and value to the database
        """

        if key in self.myDict and value not in self.myDict[key]:
            self.myDict[key].append(value)
        else:
            self.myDict[key] = [value]

    def removeEntry(self):
        print("Please implement me")



