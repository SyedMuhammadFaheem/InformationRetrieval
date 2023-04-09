import Queries
import math

'''This class is responsible for the creation of document vectors with dimensions 
equal to the number of words present in the dictionary. It then writes all the 
document vectors in text file to avoid re calculations leading towards increased
complexity.'''


class VectorProcessing:

    # constructor to initialize a list for document vectors to be stored.
    def __init__(self):
        self.__docVectors = []

    # loads the positional index, reads all the words from the dictionary and calculates the td idf values for each word in a specific document.
    def makeVectors(self):
        QueryObj = Queries.Queries()
        QueryObj.printPositionalIndex()
        QueryObj.loadPositionalIndex()
        words = QueryObj.getWords()
        for i in range(30):
            docVec = []
            for keys, values in words.items():
                keys = keys
                df = len(values[0])
                if i+1 in values[0]:
                    # represents term frequency which is the occurence of word in a single document.
                    tf = len(values[0][i+1])
                else:
                    tf = 0
                # represents inverse document frequency which is the ratio of number of documents and document frequency.
                idf = math.log10(30/df)
                docVec.append(tf*idf)
            self.__docVectors.append(docVec)

    # writes all the produced document vectors in a text file for the purpose of preprocessing
    def writeToFile(self):
        fileVectors = open("documentVectors.txt", "w")
        for vector in self.__docVectors:
            fileVectors.write(str(vector)+'\n')
        fileVectors.close()
