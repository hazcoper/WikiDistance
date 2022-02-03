# WikiDistance
measure the distance between two different wikipedia articles




things to keep in mind

will need a front end, probably a website where people will give the links, and the program will return the distance
    would be good to use the users to index wikepedia


how will we store the data?
how will we search the data?
how will we update the data?
how are we going to make the request?


would be cool to generate statistics

how many links per page?


there are two approaches that I could take:
    starting from the source, get all of the links, go to each of the links and do the same, until we reach the final link
    there are around 300 links in each page
    this could be done with threads but the growth is still a lot
    would only be possible if there was a way to rate the links by relevance, and search those first
        find some heuristic to determine which link is closer without looking at it
        maybe look at categories?

    the other way is to create a database where all of the articles are indexed
    and use that to search
    this database could be built over time
    around 6 million articles
    it would be good to make a decentralized way to build and maintain the database
    many nodes querying wikipedia, sending the info to the data base to be appended or updated
    might have problems with request limit



store
    to store the dictionary we have two options
    serialize or using json


vocabulary:
    source --> the starting article
    dest   --> the final article


dictionary:
    key -> article name -> needs to contain a date to keep track of when was updated
    value -> list of articles


vou poder ter n dicionarios carregados em memoria

cada vez que recebo uma coisa:
	vejo qual e a letra inicial
	vejo se esta carregado em memoria ou nao
		se nao tiver
			vou tirar um da minha lista e carregar


implementar algoritmo de compresao de dados com a lista


dar um nome a cada pedaco do dicionario
	right now estao divididos por letras



check if I am not always getting the same thing with andre