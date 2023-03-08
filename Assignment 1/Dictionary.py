import Dataset 
import re
import string
import unidecode
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import contractions

class Dictionary:
    __words={}
    __stopWords=[]

    def __init__(self):
        self.__words={}
        self.__stopWords=[]
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer=PorterStemmer()
        self.punctuation_table = str.maketrans('','',string.punctuation)
    
    def readStopWords(self):        #stopwords file reading
        with open('Stopword-List.txt') as file:
            lines=file.readlines()
        for line in lines:
            self.__stopWords.append(line[:len(line)-1])

    def removeStopWords(self,words):
        self.readStopWords()
        filtered=[word for word in words if word not in self.__stopWords]
        return filtered
    
    def removeWhiteSpaces(self,text):
        return re.sub(' +',' ', text)
    
    def lowerText(self,text):
        return text.lower()
    
    def removeContractions(self,words):
        contracted=[]
        for word in words:
            contracted.append(contractions.fix(word))
        return contracted

    def removePunctuations(self,sentence):
        return sentence.translate(self.punctuation_table)

    def wordTokenize(self,sentence,fileNum):
        words=word_tokenize(sentence)
        words=self.removeContractions(words)
        words=self.lemmatizeWords(words)
        words=self.removeStopWords(words)
        self.appendDictionary(words,fileNum)
   
    def lemmatizeWords(self,words):
        # filtered=[self.stemmer.stem(word) for word in words]
        filtered = [self.lemmatizer.lemmatize(word) for word in words]
        return filtered
    
    def appendDictionary(self,words,fileNum):
        for index,word in enumerate(words):
            if word not in string.ascii_lowercase:
                filtered=[]
                for letter in word:
                    if letter in string.ascii_lowercase:
                        filtered.append(letter)
                word=''.join(filtered) 
            if len(word)>2:
                if word in self.__words:
                    if fileNum in self.__words[word][0]:
                        self.__words[word][0][fileNum].append(index)
                    else:
                        self.__words[word][0][fileNum]=[index]
                else:
                    self.__words[word]=[]
                    self.__words[word].append({})
                    self.__words[word][0][fileNum]=[index]
  
    def removePunctuation(self,sentence):
        return sentence.translate(self.punctuation_table)
    
    def tokenizeSentences(self,text,fileNum):
        sentences = sent_tokenize(text)
        for sentence in sentences:
            sentence=self.removePunctuation(sentence)
            sentence=sentence.strip()
            self.wordTokenize(sentence,fileNum)
                
    def documentProcessing(self):
        fileObj=Dataset.Dataset()
        fileObj.readDataset()
        files=fileObj.getFiles()
        fileNum=1
        for doc in files:
            text = self.removeWhiteSpaces(doc)
            text = unidecode.unidecode(text)
            text = self.lowerText(text)
            self.tokenizeSentences(text,fileNum)
            fileNum+=1
        self.__words=dict(sorted(self.__words.items(),key=lambda x:x[0]))
    
    def printPostingList(self):
        for keys,values in self.__words.items():
            print(keys,values)

    def writeToFile(self):
        fileDict = open("dictionary.txt", "w")
        filePosting = open("postings.txt", "w")
        for keys,values in self.__words.items():
            fileDict.write(keys+'\n')
            filePosting.write(str(values)+'\n')   
        fileDict.close()
        filePosting.close()




