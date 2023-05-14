import PreProcessingFiles as ppf
import Clustering as clustering


"""This module acts like the controller program. To run this code, 
simply write 'python3 main.py' (for linux users) or 'python main.py' 
(for windows users). The commented code is for testing purposes. 
If you wish to remove it, you can, but let it be xD"""


# objPreProcess = ppf.PreProcessing()
# objPreProcess.documentProcessing()

objCluster = clustering.Clustering()
groundTruth = objCluster.getGroundTruthClasses()
pur = []
for i in range(25):
    clusters = objCluster.KMeansClustering(i, 5)
    nClusters = 5

    purity = objCluster.calculatePurity(groundTruth, clusters)
    pur.append(purity)

purity = max(pur)

clusters = sorted(clusters.items())
for keys, vals in clusters:
    print("Class", keys + 1, vals)

print("\nPurity using tf-idf baseline:", purity)
