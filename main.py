import json
import os

class MyDatabse():

    def __init__(self):
        self.myDict = {}

        self.fileName = None

        self.loadDict()


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
            print("No file found")
            return
         
        with open(jsonList[0], "r") as read_file:
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

    def saveDict(self):
        """
        Will save the dictionary
        """
        if self.fileName == None:
            self.fileName = self.searchDir()
        
        #save to the file (overwritting)
        with open(fileName, "w") as write_file:
            json.dump(self.myDict, write_file)

    def getDictSize(self):
        print("Please implement me")

    #search



