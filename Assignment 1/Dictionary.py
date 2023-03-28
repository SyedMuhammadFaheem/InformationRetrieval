import Dataset
import re
import string
import unidecode
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import contractions


'''This class is responsible for the retrieval of the documents from the 
stored variable and then performs the relevant processes to tokenize 
then normalize the tokens through stemming, lemmatization, removing stop 
words etc'''


class Dictionary:
    __words = {}
    __stopWords = []

    def __init__(self):
        self.__words = {}
        self.__stopWords = []
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.punctuation_table = str.maketrans('', '', string.punctuation)

    # reading the stopwords from the file provided
    def readStopWords(self):
        with open('Stopword-List.txt') as file:
            lines = file.readlines()
        for line in lines:
            self.__stopWords.append(line[:len(line)-1])

    # checks if the specific token is equal to stop words then it doesn't get included in the positional index
    def removeStopWords(self, words):
        self.readStopWords()
        filtered = [word for word in words if word not in self.__stopWords]
        return filtered

    # removes the extra white spaces from the sentence so that tokenization can be made easier
    def removeWhiteSpaces(self, text):
        return re.sub(' +', ' ', text)

    # turns the uppercase english letters into lowercase to serve in normalization purposes
    def lowerText(self, text):
        return text.lower()

    # converts the specific token into more of its existing morphological forms to increase precision and recall side by side
    def removeContractions(self, words):
        contracted = []
        for word in words:
            contracted.append(contractions.fix(word))
        return contracted

    # converts a single sentence into words based on some specific criteria
    def wordTokenize(self, sentence, fileNum):
        words = word_tokenize(sentence)
        words = self.removeContractions(words)
        words = self.lemmatizeWords(words)
        words = self.removeStopWords(words)
        self.appendDictionary(words, fileNum)

    # helps in the process of lemmatization to improve precision and also stemming which improves recall
    def lemmatizeWords(self, words):
        filtered1 = [self.stemmer.stem(word) for word in words]
        filtered2 = [self.lemmatizer.lemmatize(word) for word in words]
        return filtered1+filtered2

    # after all the necessary processes the word gets appended to the dictionary after checking if its not already present in the dictionary. If it is present, then only the document no. gets appended to the dictionary along with its position in the document
    def appendDictionary(self, words, fileNum):
        for index, word in enumerate(words):
            if word not in string.ascii_lowercase:
                filtered = []
                for letter in word:
                    if letter in string.ascii_lowercase:
                        filtered.append(letter)
                word = ''.join(filtered)
            if len(word) > 2:
                if word in self.__words:
                    if fileNum in self.__words[word][0]:
                        if index not in self.__words[word][0][fileNum]:
                            self.__words[word][0][fileNum].append(index)
                    else:
                        self.__words[word][0][fileNum] = [index]
                else:
                    self.__words[word] = []
                    self.__words[word].append({})
                    self.__words[word][0][fileNum] = [index]
        self.__words=dict(sorted(self.__words.items()))

    # removes the punctuations which include fullstops, commas, and inverted commas to avoid leaving behind of important words
    def removePunctuation(self, sentence):
        return sentence.translate(self.punctuation_table)

    # converts one whole document into sentence pieces after which further processing is done
    def tokenizeSentences(self, text, fileNum):
        sentences = sent_tokenize(text)
        for sentence in sentences:
            sentence = self.removePunctuation(sentence)
            # strip method used to removed trailing or leading whitespaces if any
            sentence = sentence.strip()
            self.wordTokenize(sentence, fileNum)

    # reads all the files and provide with necessary function callings to tokenize and normalize the documents one by one
    def documentProcessing(self):
        fileObj = Dataset.Dataset()
        fileObj.readDataset()
        files = fileObj.getFiles()
        fileNum = 1
        for doc in files:
            text = self.removeWhiteSpaces(doc)
            text = unidecode.unidecode(text)
            text = self.lowerText(text)
            self.tokenizeSentences(text, fileNum)
            fileNum += 1
        self.__words = dict(sorted(self.__words.items(), key=lambda x: x[0]))

    # utility function to get a view of the positional index
    def printPostingList(self):
        for keys, values in self.__words.items():
            print(keys, values)

    # used to write the dictionary and posting list in a file to provide with pre processing feature and faster execution of the query
    def writeToFile(self):
        fileDict = open("dictionary.txt", "w")
        filePosting = open("postings.txt", "w")
        for keys, values in self.__words.items():
            fileDict.write(keys+'\n')
            filePosting.write(str(values)+'\n')
        fileDict.close()
        filePosting.close()
