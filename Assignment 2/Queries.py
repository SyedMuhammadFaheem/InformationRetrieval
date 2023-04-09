import ast
import numpy as np
import math
from pathlib import Path

'''This class is repsonsible for the query processing techniques used in 
vector space model. It includes functions to calculate query vector, cosine similarity
and partial matching in the documents. It also includes functionality to rank the
documents according to their cosine scores.'''


class Queries:
    __words = {}
    __resultSet = []

    def __init__(self):
        self.__words = {}
        self.__resultSet = []

    # loads the pre processed dictionary terms and posting list along with the positional index from a file
    def loadPositionalIndex(self):
        fileDict = open("dictionary.txt", "r")
        filePosting = open("postings.txt", "r")
        while fileDict and filePosting:
            word = fileDict.readline()
            word = word[:len(word)-1]
            posting = filePosting.readline()
            posting = posting[:len(posting)-1]
            if word and posting:
                self.__words[word] = []
                self.__words[word].append(
                    ast.literal_eval(posting[1:len(posting)-1]))
            else:
                break
        fileDict.close()
        filePosting.close()

    # getter function to retrieve all the words generated from the dictionary
    def getWords(self):
        return self.__words

    # overloaded function serving the same task of partial matching with one argument as a string and the other as a list
    def unionQuery(self, term1, intermediateResult: list):
        result = []
        if term1 in self.__words:
            result += list(self.__words[term1][0].keys())
        result += intermediateResult
        return sorted(list(set(result)))

    # used to check partial matching in all the documents for two terms
    def unionQuery(self, term1, term2):
        result = []
        if term1 in self.__words:
            result += list(self.__words[term1][0].keys())
        if term2 in self.__words:
            result += list(self.__words[term2][0].keys())
        return sorted(list(set(result)))

    # used to check partial matching in all the documents for a single term
    def unionQueryOne(self, term):
        result = []
        if term in self.__words:
            result += list(self.__words[term][0].keys())
        return sorted(list(set(result)))

    # main function which calls the appropriate function considering if the query contains single term, dual terms or multiple terms
    def orQuery(self, queryList):
        result = []
        i = 0
        while i < len(queryList):
            if result:
                result = list(set(self.unionQuery(queryList[i], result)))
                i += 1
            elif len(queryList) > 1:
                result.append(self.unionQuery(
                    queryList[i], queryList[i+1]))
                i += 2
            else:
                result.append(self.unionQueryOne(queryList[i]))
                i += 1
        return result

    # used to calculate term frequency and document frequence including idf and make a query vector out of it.
    def weightQuery(self, query):
        querySet = set(query)
        queryDict = dict()
        queryVector = []
        for word in querySet:
            count = 0
            for wordFromList in query:
                if word == wordFromList:
                    count += 1
            queryDict[word] = count
        for keys, values in self.__words.items():
            tf = 0
            df = len(values[0])
            if keys in queryDict:
                tf = queryDict[keys]
            idf = math.log10(30/df)
            queryVector.append(tf*idf)
        return queryVector

    # used to retrieve the relevant document vectors after partial matching has been done to manage the time and space complexity
    def loadDocumentVectors(self, intersectResult):
        documentVectors = open('documentVectors.txt', 'r')
        docVectors = []
        docTrack = []
        dump = 1
        i = 1
        while documentVectors:
            if i in intersectResult:
                vector = documentVectors.readline()
                vector = vector[:len(vector)-1]
                vector = ast.literal_eval(vector)
                docVectors.append(vector)
                docTrack.append(i)
            else:
                dump = documentVectors.readline()
            if dump:
                i += 1
            else:
                break
        documentVectors.close()
        return docVectors, docTrack

    # used to calculate cosine similarity between docoument vectors and query vector one by one. Cosine-Similarity = document-vector.query-vector/(|document-vector|*|query-vector|)
    def cosineSimilarity(self, queryVector, docVectors):
        rankVector = []
        for vector in docVectors:
            i, j = 0, 0
            resultantVector = []
            while i < len(vector):
                resultantVector.append(vector[i]*queryVector[j])
                i += 1
                j += 1
            sum = 0
            for val in resultantVector:
                sum += val
            docRes = 0
            for docVal in vector:
                docRes += math.pow(docVal, 2)
            docRes = math.sqrt(docRes)
            queryRes = 0
            for queryVal in queryVector:
                queryRes += math.pow(queryVal, 2)
            queryRes = math.sqrt(queryRes)
            rankVector.append(sum/(queryRes*docRes))
        return rankVector

    # controller function which processes the query, finds partial matching of the query and then cosine similarities. Afterwards, the cosine similarities retrieved are sorted and then appended to the result set.
    def queryProcessing(self, query):
        query = query.lower()
        queryList = []
        splitQuery = []
        splitQuery = query.split()
        if splitQuery:
            for word in splitQuery:
                if len(word) > 2 and word != ' ':
                    queryList.append(word)
        intersectResult = self.orQuery(queryList)
        if intersectResult:
            intersectResult = [doc for doc in intersectResult[0]]
        queryVector = self.weightQuery(splitQuery)
        docVectors, docTrack = self.loadDocumentVectors(intersectResult)
        rankVector = self.cosineSimilarity(queryVector, docVectors)
        tempRank = np.array(rankVector)
        tempDocs = np.array(docTrack)
        sort = np.argsort(tempRank)
        docTrack = list(tempDocs[sort])
        rankVector = list(tempRank[sort])
        i = len(docTrack)-1
        print('Query:', query)
        print(sorted(rankVector, reverse=True))
        while i >= 0:
            if rankVector[i]+0.001 >= 0.05:
                self.__resultSet.append(docTrack[i])
            i -= 1
        rankVector = sorted(rankVector, reverse=True)
        return self.__resultSet

    # utility function to print the result sets of queries entered. (Never called and only used as a debugging tool)
    def writeToFile(self, query, rankVector):
        path = Path('results.txt')
        if path.is_file():
            resultFile = open('results.txt', 'a')
        else:
            resultFile = open('results.txt', 'w')
        resultFile.write(query+'\n')
        resultFile.write(str(self.__resultSet)+'\n')
        resultFile.write(str(rankVector[:len(self.__resultSet)])+'\n')

    # prompts the user to enter query as input
    def queryInput(self, query):
        return self.queryProcessing(query.lower())

    # prints the resultant document set
    def generateResultSet(self):
        print('Result-Set:', self.__resultSet)

    # utility function to view the positional index
    def printPositionalIndex(self):
        for keys, values in self.__words.items():
            print(keys, values)
