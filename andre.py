#!/usr/bin/python3

import requests
import time
from Database import MyDatabase


myDatabase = MyDatabase()
start = time.time()

S = requests.Session()

def do_request(article):
    notDone = True

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "titles": article,
        "action": "query",
        "format": "json",
        "prop": "links",
        "pllimit": "max"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()


    
    # if notDone:
    #     PARAMS ["plcontinue"] = "plcontinue"

    # if "continue" in DATA:
    #     print("This is continue")
    #     plcontinue = DATA["continue"]["plcontinue"]

    return DATA

def format_request(data):
    print(data)
    PAGES = data["query"]["pages"]

    i = 0
    for k, v in PAGES.items():
        for l in v["links"]:
            i += 1
            print(f"{i}:{l['title']}")

def main():
    data = do_request("Portugal")
    
    # for entry in data["query"]["pages"]["23033"]["links"]:
    #     if entry["title"] ==".pt":
    #         continue
        
    #     myDatabase.addEntry("Portugal",entry["title"])

    # print("this is the data")
    # print(type(data))
    print(data)
    # print(data.keys())
    # print(data["query"])

    # format_request(data)

if __name__ == '__main__':
    main()
    myDatabase.saveDict()

print(f"Time:{time.time() - start}")