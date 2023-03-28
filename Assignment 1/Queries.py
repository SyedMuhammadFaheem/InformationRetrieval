import ast

'''This class is repsonsible for the query processing techniques used in 
boolean retrieval model. It includes functions to cater intersection, union
and not operator query. It also includes functionality to handle proximity
queries as well.'''


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

    # handles the one word query with no indulgence of booelean operators
    def simpleQuery(self, term):
        if term in self.__words:
            return list(self.__words[term][0].keys())
        return []

    # handles the query containing NOT operator
    def notQuery(self, term):
        if term in self.__words:
            presentDocs = list(self.__words[term][0].keys())
        result = []
        i = 1
        while i <= 30:
            if i < len(presentDocs) and presentDocs[i] == i:
                continue
            else:
                result.append(i)
            i += 1
        return result

    # handles the query containing OR operator
    def orQuery(self, term1, term2):
        result = []
        if term1 in self.__words:
            result += list(self.__words[term1][0].keys())
        if term2 in self.__words:
            result += list(self.__words[term2][0].keys())
        return sorted(list(set(result)))

    # handles the query containing AND operator
    def andQuery(self, term1, term2):
        result = []
        i, j = 0, 0
        if term1 in self.__words:
            termKeyOne = list(self.__words[term1][0].keys())
        if term2 in self.__words:
            termKeyTwo = list(self.__words[term2][0].keys())
        if term1 not in self.__words or term2 not in self.__words:
            return []
        while i < len(self.__words[term1][0]) and j < len(self.__words[term2][0]):
            if termKeyOne[i] == termKeyTwo[j]:
                result.append(termKeyOne[i])
                i += 1
                j += 1
            elif termKeyOne[i] < termKeyTwo[j]:
                i += 1
            else:
                j += 1
        return result

    # function for developer's utility where one parameter is a list and the other is a dictionary term. It also handles the query with AND operator
    def specialAndQuery(self, tempList, term):
        result = []
        i, j = 0, 0
        if term in self.__words:
            termKeyOne = list(self.__words[term][0].keys())
        if term not in self.__words or len(tempList) == 0:
            return []
        while i < len(self.__words[term][0]) and j < len(tempList):
            if termKeyOne[i] == tempList[j]:
                result.append(termKeyOne[i])
                i += 1
                j += 1
            elif termKeyOne[i] < tempList[j]:
                i += 1
            else:
                j += 1
        return result

    # function for developer's utility where one parameter is a list and the other is a dictionary term. It also handles the query with OR operator
    def specialOrQuery(self, tempList, term):
        result = []
        if term in self.__words:
            result += list(self.__words[term][0].keys())
        if tempList:
            result += tempList
        return sorted(list(set(result)))

    # function for developer's utility where both parameters are a list containing intermediate results for a part of the query. It also handles the query with AND operator
    def postingAndQuery(self, tempList1, tempList2):
        result = []
        i, j = 0, 0
        if len(tempList1) == 0 or len(tempList2) == 0:
            return []
        while i < len(tempList1) and j < len(tempList2):
            if tempList1[i] == tempList2[j]:
                result.append(tempList1[i])
                i += 1
                j += 1
            elif tempList1[i] < tempList2[j]:
                i += 1
            else:
                j += 1
        return result

    # function for developer's utility where both parameters are a list containing intermediate results for a part of the query. It also handles the query with OR operator
    def postingOrQuery(self, tempList1, tempList2):
        result = []
        if tempList1:
            result += tempList1
        if tempList2:
            result += tempList2
        return sorted(list(set(result)))

    # handles the proximity query consisting of 2 dictionary terms and 'k' pointing to the distance between the words.
    def proximityQuery(self, term1, term2, k):
        result = []
        temp = self.andQuery(term1, term2)
        index1 = []
        index2 = []
        for doc in temp:
            index1 = self.__words[term1][0][doc]
            index2 = self.__words[term2][0][doc]
            i = 0
            while i < len(index1):
                for j in range(len(index2)):
                    if index1[i]+k+1 == index2[j] or index1[i]+k == index2[j]  or index2[j]+k+1 == index1[i] or index2[j]+k == index1[i]:
                        if doc not in result:
                            result.append(doc)
                i += 1
        return result

    # controller function which determines the type of query being entered and calling the appropriate functions to provide with the result set
    def queryProcessing(self, query):
        query = query.lower()
        if len(query) > 1:
            splitQuery = query.split(' ')
        check = False
        k = splitQuery[-1]
        kIndex = ''
        for letter in k:
            if letter != '\\':
                kIndex += letter
            if letter == '\\':
                check = True
        if check:
            kIndex = int(kIndex)
            self.__resultSet = self.proximityQuery(
                splitQuery[0], splitQuery[1], kIndex)
            return self.__resultSet

        operators = ['and', 'or', 'not']
        i = 0
        if len(splitQuery) == 1:
            self.__resultSet = self.simpleQuery(query)
        elif len(splitQuery) == 2:
            if splitQuery[0] == 'not':
                self.__resultSet = self.notQuery(splitQuery[1])
        elif len(splitQuery) == 3:
            if splitQuery[1] == 'and':
                self.__resultSet = self.andQuery(splitQuery[0], splitQuery[2])
            elif splitQuery[1] == 'or':
                self.__resultSet = self.orQuery(splitQuery[0], splitQuery[2])
        elif len(splitQuery) == 4:
            temp = []
            if splitQuery[0] == 'not':
                if splitQuery[1] not in operators:
                    temp = self.notQuery(splitQuery[1])
                if splitQuery[2] == 'and':
                    self.__resultSet = self.specialAndQuery(
                        temp, splitQuery[2])
                elif splitQuery[2] == 'or':
                    self.__resultSet = self.specialOrQuery(temp, splitQuery[2])
            elif splitQuery[2] == 'not':
                if splitQuery[3] not in operators:
                    temp = self.notQuery(splitQuery[3])
                if splitQuery[0] == 'and':
                    self.__resultSet = self.specialAndQuery(
                        temp, splitQuery[0])
                elif splitQuery[0] == 'or':
                    self.__resultSet = self.specialOrQuery(temp, splitQuery[0])
        elif len(splitQuery) == 5:
            temp = []
            if splitQuery[1] == 'and':
                if splitQuery[0] and splitQuery[2] not in operators:
                    temp = self.andQuery(splitQuery[0], splitQuery[2])
                    if splitQuery[3] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[4])
                    elif splitQuery[3] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[4])
            elif splitQuery[1] == 'or':
                if splitQuery[0] and splitQuery[2] not in operators:
                    temp = self.orQuery(splitQuery[0], splitQuery[2])
                    if splitQuery[3] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[4])
                    elif splitQuery[3] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[4])

        elif len(splitQuery) == 6:
            notTemp = []
            temp = []
            check = 0
            if splitQuery[0] == 'not':
                check = 1
                if splitQuery[1] not in operators:
                    notTemp = self.notQuery(splitQuery[1])
            elif splitQuery[2] == 'not':
                check = 2
                if splitQuery[2] not in operators:
                    notTemp = self.notQuery(splitQuery[2])
            elif splitQuery[4] == 'not':
                check = 3
                if splitQuery[4] not in operators:
                    notTemp = self.notQuery(splitQuery[4])
            if check == 1:
                if splitQuery[2] == 'and':
                    if splitQuery[3] not in operators:
                        temp = self.specialAndQuery(notTemp, splitQuery[3])
                        if splitQuery[4] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[5])
                        elif splitQuery[4] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[5])
                elif splitQuery[2] == 'or':
                    if splitQuery[3] not in operators:
                        temp = self.specialOrQuery(notTemp, splitQuery[3])
                        if splitQuery[4] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[5])
                        elif splitQuery[4] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[5])
            elif check == 2:
                if splitQuery[1] == 'and':
                    if splitQuery[0] not in operators:
                        temp = self.specialAndQuery(notTemp, splitQuery[0])
                        if splitQuery[5] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[6])
                        elif splitQuery[5] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[6])
                elif splitQuery[1] == 'or':
                    if splitQuery[0] not in operators:
                        temp = self.specialOrQuery(notTemp, splitQuery[0])
                        if splitQuery[5] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[6])
                        elif splitQuery[5] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[6])
            elif check == 3:
                if splitQuery[3] == 'and':
                    if splitQuery[2] not in operators:
                        temp = self.specialAndQuery(notTemp, splitQuery[2])
                        if splitQuery[1] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[0])
                        elif splitQuery[1] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[0])
                elif splitQuery[3] == 'or':
                    if splitQuery[2] not in operators:
                        temp = self.specialOrQuery(notTemp, splitQuery[2])
                        if splitQuery[1] == 'or':
                            self.__resultSet = self.specialOrQuery(
                                temp, splitQuery[0])
                        elif splitQuery[1] == 'and':
                            self.__resultSet = self.specialAndQuery(
                                temp, splitQuery[0])
        elif len(splitQuery) == 7:
            notTemp1 = []
            notTemp2 = []
            temp = []
            check = 0
            if splitQuery[0] == 'not' and splitQuery[3] == 'not':
                check = 1
                if splitQuery[1] not in operators:
                    notTemp1 = self.notQuery(splitQuery[1])
                if splitQuery[3] not in operators:
                    notTemp2 = self.notQuery(splitQuery[3])
            elif splitQuery[3] == 'not' and splitQuery[5] == 'not':
                check = 2
                if splitQuery[3] not in operators:
                    notTemp1 = self.notQuery(splitQuery[3])
                if splitQuery[5] not in operators:
                    notTemp2 = self.notQuery(splitQuery[5])
            elif splitQuery[0] == 'not' and splitQuery[5] == 'not':
                check = 3
                if splitQuery[0] not in operators:
                    notTemp1 = self.notQuery(splitQuery[0])
                if splitQuery[5] not in operators:
                    notTemp2 = self.notQuery(splitQuery[5])
            if check == 1:
                if splitQuery[2] == 'and':
                    temp = self.postingAndQuery(notTemp1, notTemp2)
                    if splitQuery[5] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[6])
                    elif splitQuery[5] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[6])
                elif splitQuery[2] == 'or':
                    temp = self.postingOrQuery(notTemp1, notTemp2)
                    if splitQuery[5] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[6])
                    elif splitQuery[5] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[6])
            elif check == 2:
                if splitQuery[3] == 'and':
                    temp = self.postingAndQuery(notTemp1, notTemp2)
                    if splitQuery[1] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[0])
                    elif splitQuery[1] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[0])
                elif splitQuery[3] == 'or':
                    temp = self.postingOrQuery(notTemp1, notTemp2)
                    if splitQuery[1] == 'or':
                        self.__resultSet = self.specialOrQuery(
                            temp, splitQuery[0])
                    elif splitQuery[1] == 'and':
                        self.__resultSet = self.specialAndQuery(
                            temp, splitQuery[0])
            elif check == 3:
                if splitQuery[2] == 'and':
                    if splitQuery[3] not in operators:
                        temp = self.specialAndQuery(notTemp1, splitQuery[3])
                    if splitQuery[4] == 'or':
                        self.__resultSet = self.postingOrQuery(temp, notTemp2)
                    elif splitQuery[4] == 'and':
                        self.__resultSet = self.postingAndQuery(temp, notTemp2)
                elif splitQuery[2] == 'or':
                    if splitQuery[3] not in operators:
                        temp = self.specialOrQuery(notTemp1, splitQuery[3])
                    if splitQuery[4] == 'or':
                        self.__resultSet = self.postingOrQuery(temp, notTemp2)
                    elif splitQuery[4] == 'and':
                        self.__resultSet = self.postingAndQuery(temp, notTemp2)
        elif len(splitQuery) == 8:
            notTemp1 = []
            notTemp2 = []
            notTemp3 = []
            temp = []
            if splitQuery[0] == 'not' and splitQuery[3] == 'not' and splitQuery[6] == 'not':
                if splitQuery[1] and splitQuery[4] and splitQuery[7] not in operators:
                    notTemp1 = self.notQuery(splitQuery[1])
                    notTemp2 = self.notQuery(splitQuery[4])
                    notTemp3 = self.notQuery(splitQuery[7])
            if splitQuery[2] == 'and':
                temp = self.postingAndQuery(notTemp1, notTemp2)
                if splitQuery[5] == 'or':
                    self.__resultSet = self.postingOrQuery(temp, notTemp3)
                elif splitQuery[5] == 'and':
                    self.__resultSet = self.postingAndQuery(temp, notTemp3)
            elif splitQuery[2] == 'or':
                temp = self.postingOrQuery(notTemp1, notTemp2)
                if splitQuery[5] == 'or':
                    self.__resultSet = self.postingOrQuery(temp, notTemp3)
                elif splitQuery[5] == 'and':
                    self.__resultSet = self.postingAndQuery(temp, notTemp3)
        return self.__resultSet

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
