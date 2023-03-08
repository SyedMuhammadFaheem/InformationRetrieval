
class Dataset:
    __files=[]
    
    def __init__(self):
        self.__files=[]
    
    def readDataset(self):         #reading data set
        for i in range(30):
            filename='CricketReviews/' + str(i+1) + '.txt'
            lines=[]
            with open(filename) as file:
                lines=file.readlines()
            tempDoc=''
            for line in lines:
                if line=='\n':
                    continue
                if '\n' in line:
                    tempDoc+=line.replace('\n','. ')
                else:
                    tempDoc+=line
            self.__files.append(tempDoc)
    
    def getFiles(self):
        return self.__files
    
    