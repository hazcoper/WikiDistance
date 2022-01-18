
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re

import time

start = time.time()
url = "https://en.wikipedia.org/wiki/Pillars_of_Creation"


pattern = "((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"



soup = BeautifulSoup(urlopen(url))
print("hello")
end = time.time()
print(end - start)

# for link in soup.find_all("a", href=True):
    # print(link["href"], link.get_text())


"""
o melhor approach e fazer index da wikipedia toda em vez de ir fazendo recursivo
"""