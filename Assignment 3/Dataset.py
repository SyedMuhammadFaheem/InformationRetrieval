import glob

"""This class is responsible for the retrieval of intact documents from the 
cricket reviews dataset. This class consists of two methods, readDataset() and getFiles()."""


class Dataset:
    __files = []

    def __init__(self):  # constructor to initialize class object and files list as empty
        self.__files = dict()

    def readDataset(self):  # reading data set file by file and storing as a list
        filename = glob.glob("Doc50/*")
        for i in range(50):
            lines = []
            with open(filename[i]) as file:
                lines = file.readlines()
            tempDoc = ""
            for line in lines:
                if line == "\n":
                    continue
                if "\n" in line:
                    tempDoc += line.replace("\n", ". ")
                else:
                    tempDoc += line
            self.__files[int(filename[i][6:])] = tempDoc

    def getFiles(self,):  # used for retrieving the dataset since the instance is kept as private
        return self.__files
