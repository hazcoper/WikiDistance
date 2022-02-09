#!/usr/bin/python3

import requests
import time
from Database import MyDatabase
import threading
import signal

from pprint import pprint

blackist = ["Help:", "Category:", "Talk:", "Wikipedia:", "Template:", "Template talk", "Portal:"]


keepWorking = True
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



def worker(name):
    global keepWorking

    while keepWorking:
        
        #wait for the database to give me something
        baseArticle = myDatabase.getBaseArticle()
        if baseArticle == False:
            print(f"[THREAD{name}] - Waiting for links")
            time.sleep(1)
            continue

        #means that I already have an article
        print(f"[THREAD{name}] - Starting {baseArticle} links")
        
        
        #for each article in link list
        #   get the links for the article
        #   add the article and the links to the database
        #mark the base article
        articleSet = myDatabase.getLinks(baseArticle)

        for article in articleSet:
            data, c = do_request(article)
            myDatabase.appendReferenceList(article, data)
            print(f"[THREAD{name}] - {baseArticle} - Did {article} {c} links")

        myDatabase.markArticle(baseArticle)

    print(f"[THREAD{name}] - Got close signal, not repeating")


def exit_handler(signum, frame):
    global keepWorking
    print("[MAIN] - got closing signal")
    keepWorking = False

def main():

    global keepworking

    #does it make a difference putting it before making the threads or not?
    signal.signal(signal.SIGINT, exit_handler)


    if myDatabase.isEmpty():
        #if it is empty than we should add something
        print(f"[MAIN] - db empty need to add something")
        baseLink = "Rubicon"
        data, c = do_request(baseLink)
        myDatabase.appendReferenceList(baseLink, data)


    #lets create the threads
    counter = 0
    for i in range(10):
        t = threading.Thread(target=worker, args=(counter,))
        t.start()
        counter += 1


    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

            
if __name__ == '__main__':
    main()
    myDatabase.saveAndExit()

print(f"Time:{time.time() - start}")

"""

ideia 1 -> nao usada
    preciso de pensar como e que eu vou fill in the database com threads


    vou buscar um artigo
        vejo todos os links desse artigo
        faco uma lista e divido em x partes
        dou cada uma das parte para as threads

        portanto as threads vao receber uma lista de artigos
            para cada artigo nessa lista, vou buscar os links nesses artigo


        basicamnete eu vou ter uma thread que vai estar a processar base articles
            depois vou ter x thread que vao estar a buscar os links de cada link desses artigos

        de certeza que isto nao e a maneira mais eficiente, mas e capaz de funcionar


        vou ter x listas
        para cada lista vou ter um lock
        nessas listas vou adicionar os links da base
        vou dividir isso

    base1
        link1
        link2
        link3

    link1
        link2
        link5
        link6



ideia 2 -> nao usada
    meu buffer vai ter um tamanho fixo
        as threads vao estar constantemente a ir la, buscar artigos (esses artigos vao conter uma lista de links)
            para cada link nessa lista de links
    tenho a base thread que vai buscasr um artigo base
        a ir buscar esse artigo base, vai adicionar a base de dados
        mas tambem vai adicionar a lista de links ao buffer



ideia 3 -> usada
    cada thread vai fazer a mesma coisa
        
        1. pedir a base de dados um artigo
            esperar ate receber alguma coisa da base de dados

        2. quando tiver recebido o meu base article
            para cada artigo dentro do base article:
                vou buscar todos os links desse artigo
                adicionar a base de dados
            marcar artigo base como lido
        
        3. voltar para o passo 1

    tenho de perceber como vou fazer para fechar o programa
    tenho de perceber como vou fazer para iniciar o programa
        pela a primeira vez quando a base de dados esta vazia


    para fechar o programa
        vou apanhar o sinal na base thread
        mandar o sinal a todas as outras threads
        elas vao acabar o que estao a fazer e depois parar
            se calhar basta ter uma variavel que e tipo quit
            e cada vez antes de pedir uma coisa a base de dados vou ver se essa variave e true
    todo:
        funcao na base de dados que posso pedir um artigo para ver
            vai devolver algum artigo que nao tenha sido visto ainda
            retorna false se nao tiver artigo nenhum para ver
            de alguma maneira conseguir avisar que tem coisas
        tenho  de fazer o codigo da thread
        

"""


