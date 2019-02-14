'''
:author: Colton Freitas
:as-of: February 7th, 2019
'''

from Clustering.ClusteringFunctionStorage import movingAverageClustering
from Common.CommonValues import startDate, evalStartDate
from Common.CommonValues import modelStoragePathBase, evaluationModelStoragePathBase
from AI.StoredModelFile import StoredModelFile
from Common.Util.ConfigurationUtils import insertTicker, insertClusteredStocks
from typing import List

def translateClusteringFunction(clusteringFuncID : str):
    if (clusteringFuncID == "MD"):
        return movingAverageClustering
    else:
        raise NameError("No matching clustering functions for ID {0}".format(clusteringFuncID))

def getAndUseClusterFunction(modelConfiguration):
    modelID = modelConfiguration['General']['sModelID']
    clustFuncID = modelConfiguration[modelID]['sClusteringMethod']
    
    clustFunc = translateClusteringFunction(clustFuncID)
    
    return clustFunc(modelConfiguration)

def createStoredModelFile(modelConfiguration):
    filePath = modelStoragePathBase
    if (modelConfiguration['General']['bEvaluationTraining'] == "True"):
        filePath = evaluationModelStoragePathBase
    
    modelFile = StoredModelFile(filePath, modelConfiguration)
    return modelFile

def trainModel(ticker, modelConfiguration):
    insertTicker(modelConfiguration, ticker)
    clusteredStocks = getAndUseClusterFunction(modelConfiguration)
    insertClusteredStocks(modelConfiguration, clusteredStocks)
    
    modelFile = createStoredModelFile(modelConfiguration)
    modelFile.Train()
    modelFile.Save()
