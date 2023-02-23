import spacy
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()

class BooleanRetrievalModel:
    __words=dict()
    __files=[]
    __stopWords=[]
    __resultSet=[]
    
    def __init__(self):
        self.__files=[]
        self.__words=dict()
        self.__stopWords=[]
        self.__resultSet=[]
    
    def readDataset(self):         #reading data set
        fileNum=1
        for i in range(30):
            filename='CricketReviews/' + str(fileNum) + '.txt'
            lines=[]
            with open(filename) as file:
                lines=file.readlines()
            tempDoc=''
            for line in lines:
                if line=='\n':
                    continue
                if '\n' in line:
                    tempDoc+=line[:len(line)-2]
                else:
                    tempDoc+=line
            self.__files.append(tempDoc)
            fileNum+=1
    
    def readStopWords(self):        #stopwords file reading
        with open('Stopword-List.txt') as file:
            lines=file.readlines()
        for line in lines:
            self.__stopWords.append(line[:len(line)-2])

    def tokenization(self):         #tokenization
        fileNum=1
        for doc in self.__files:
            doc=nlp(doc)
            splitString=[token.text for token in doc]
            for word in splitString:
                if word not in self.__stopWords and len(word)>=2:
                    word=word.lower()
                    if word in self.__words:
                        if fileNum not in self.__words[word]:
                            self.__words[word].append(fileNum)
                    else:
                        self.__words[word]=[fileNum]
                    self.__words[word]=sorted(self.__words[word])
            fileNum+=1
    
    def intersectionQuery(self,termOne,termTwo):
        answer=[]
        i,j=0,0
        if termOne not in self.__words or termTwo not in self.__words:
            return []
        while i<len(self.__words[termOne]) and j<len(self.__words[termTwo]):
            if self.__words[termOne][i]==self.__words[termTwo][j]:
                answer.append(self.__words[termOne][i])
                i+=1
                j+=1
            elif self.__words[termOne][i]<self.__words[termTwo][j]:
                i+=1
            else:
                j+=1
        return answer

    def unionQuery(self,termOne,termTwo):
        result=[]
        if termOne in self.__words:
            result+=self.__words[termOne]
        if termTwo in self.__words:
            result+=self.__words[termTwo]
        result=set(result)
        return sorted(list(result))
  
    def simpleQuery(self,term):
        return self.__words[term]
    
    def queryProcessing(self,query):    #done only for two operands
        splitQuery=query.split(' ')
        i=0
        if len(splitQuery)==1:
            self.__resultSet=self.simpleQuery(splitQuery[i])
        else:
            while i<len(splitQuery):
                if splitQuery[i]=='AND':
                    self.__resultSet=self.intersectionQuery(splitQuery[i-1],splitQuery[i+1])
                    i+=1
                elif splitQuery[i]=='OR':
                    self.__resultSet=self.unionQuery(splitQuery[i-1],splitQuery[i+1])
                    i+=1
                i+=1

        self.generateResultSet()
    
    def queryInput(self):
        query=input("Enter your Boolean Query: ")
        self.queryProcessing(query)

    def generateResultSet(self):
        print('Result-Set:',self.__resultSet)
    
    def printPostingList(self):
        for keys,values in self.__words.items():
            print(keys,values)




boolObject=BooleanRetrievalModel()

boolObject.readDataset()
boolObject.readStopWords()
boolObject.tokenization()

boolObject.queryInput()




