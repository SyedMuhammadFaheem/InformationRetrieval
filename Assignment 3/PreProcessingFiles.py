import Dataset
import re
import string
import unidecode
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import contractions

"""This class is responsible for the retrieval of the documents from the 
stored variable and then performs the relevant processes to tokenize 
then normalize the tokens through stemming, lemmatization, removing stop 
words etc"""


class PreProcessing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = PorterStemmer()
        self.punctuation_table = str.maketrans("", "", string.punctuation)

    # removes the extra white spaces from the sentence so that tokenization can be made easier
    def removeWhiteSpaces(self, text):
        return re.sub(" +", " ", text)

    # turns the uppercase english letters into lowercase to serve in normalization purposes
    def lowerText(self, text):
        return text.lower()

    # checks every word if its an alphabet or number or underscore and then only adds it to the list and converts into string in the end
    def checkAlphaNumeric(self, words):
        filtered = []
        words = words.split(" ")
        for word in words:
            if word.isalnum():
                filtered.append(word)
        return " ".join(filtered)

    # after all the necessary processes the word gets appended to the dictionary after checking if its not already present in the dictionary. If it is present, then only the document no. gets appended to the dictionary along with its position in the document
    def appendProcessedFiles(self, words, fileNum):
        fileText = words
        writeFile = open(f"processedFiles/{fileNum}", "w")
        writeFile.write(fileText)

    # removes the punctuations which include fullstops, commas, and inverted commas to avoid leaving behind of important words
    def removePunctuation(self, sentence):
        return sentence.translate(self.punctuation_table)

    # reads all the files and provide with necessary function callings to tokenize and normalize the documents one by one
    def documentProcessing(self):
        fileObj = Dataset.Dataset()
        fileObj.readDataset()
        files = fileObj.getFiles()
        index = 0
        fileNum = list(files.keys())
        for doc in files.values():
            print(fileNum[index])
            text = self.removeWhiteSpaces(doc)
            text = unidecode.unidecode(text)
            text = self.lowerText(text)
            text = self.removePunctuation(text)
            text = text.strip()
            text = self.checkAlphaNumeric(text)
            self.appendProcessedFiles(text, fileNum[index])
            index += 1

