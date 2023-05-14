import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import os

"""This module serves the purpose of the application of K Means Clustering Algorithm using tf-idf baseline.
This class contains all the functions required to fetch the preprocessed documents, clusterise them and 
compare with the ground truth classes to calculate the purity."""


class Clustering:
    # initializes the class and fetches the preprocessed files
    def __init__(self):
        self.processedFiles = {}
        fileDir = glob.glob("processedFiles/*")
        for i in range(50):
            lines = []
            with open(fileDir[i]) as file:
                lines = file.readlines()
            tempDoc = ""
            for line in lines:
                tempDoc += line

            self.processedFiles[int(fileDir[i][15:])] = tempDoc

    # consists of the functionality to apply KMeans Clustering algorithm on the preprocessed news dataset
    def KMeansClustering(self, setDF, nClusters):
        tfidfVectorizer = TfidfVectorizer(
            min_df=setDF, stop_words=stopwords.words("english")
        )
        X = tfidfVectorizer.fit_transform(list(self.processedFiles.values()))
        kMeansModel = KMeans(
            n_clusters=nClusters, random_state=42, init="k-means++", n_init="auto"
        )
        kMeansModel.fit(X)
        clusterLabel = kMeansModel.labels_
        return self.getClusters(clusterLabel, list(self.processedFiles.keys()))

    # groups the documents of the same cluster using a dictionary. DISPLAYED IN THE END
    def getClusters(self, clusterLabel, fileNums):
        clusters = dict()
        i = 0
        for label in clusterLabel:
            if label not in clusters:
                clusters[label] = [fileNums[i]]
            else:
                clusters[label].append(fileNums[i])
            i += 1
        return clusters

    # fetches the ground truth classes in order to compare and contrast later
    def getGroundTruthClasses(self):
        groundTruthClasses = dict()
        for fileNum in range(5):
            fileDir = os.listdir(f"Doc50 GT/C{fileNum+1}")
            for file in fileDir:
                if fileNum + 1 not in groundTruthClasses:
                    groundTruthClasses[fileNum + 1] = [file]
                else:
                    groundTruthClasses[fileNum + 1].append(file)
        return groundTruthClasses

    # finds the class w.r.t ground truth class
    def findClass(self, groundTruth, doc):
        index = None
        for keys, vals in groundTruth.items():
            if str(doc) in vals:
                index = keys
                break
        return index

    # assigns the maximum class to the clusterised docs with the help of ground truth classes 
    def findMaxClass(self, cluster):
        maxNum = cluster[0]
        for i in range(1, len(cluster)):
            maxNum = max(maxNum, cluster[i])
        return maxNum

    # calculates the purity for the clusterised documents in comparison to ground truth
    def calculatePurity(self, gtClasses, clusters):
        holdClusters = clusters
        clusters = list(clusters.keys())
        maxClass = []

        for i in range(len(clusters)):
            clustersClass = [j * 0 for j in range(5)]
            resultantClusters = holdClusters[clusters[i]]

            for k in range(len(resultantClusters)):
                foundClass = self.findClass(gtClasses, resultantClusters[k])
                clustersClass[foundClass - 1] += 1
            maxClass.append(self.findMaxClass(clustersClass))

        sumClass = sum(maxClass)
        purity = sumClass / 50
        return purity

