
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re

import time

start = time.time()
source = "https://en.wikipedia.org/wiki/Wiki"


pattern = "((http|https)\:\/\/)mem?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"



soup = BeautifulSoup(urlopen(source))
print("hello")
end = time.time()
print(end - start)

for link in soup.find_all("a", href=True):
    myLink = link["href"]
    myText = link.get_text()

    if myLink[0] == "/":
        print(myLink)


"""
o melhor approach e fazer index da wikipedia toda em vez de ir fazendo recursivo
"""