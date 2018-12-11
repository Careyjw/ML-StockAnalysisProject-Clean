import numpy as np
from typing import List

class RNNTrainingDataStorage:

    def __init__(self, normalizationFunction, deNormalizationFunction):
        '''
        :param dataNormalizationFunction: Function to normalize the data into the range 0-inputSize
        :param dataDenormalizationFunction: Function to transform the data from the range 0-inputSize into the original data mapping
            Both denormalization and normalization functions have the same argument list, defined in :argumentList:
        :argumentList:
            (x)
            :param x: Data point to normalize/denormalize
        '''
        self.x = []
        self.y = []
        self.normalizationFunction = normalizationFunction
        self.deNormalizationFunction = deNormalizationFunction
        self.predictionData = []

    def addTrainingExample(self, x : List[List], y : List):
        self.x.append(x)
        self.y.append(y)

    def addPredictionData(self, x : List[List]):
        self.predictionData = x

    def extractPredictionData(self):
        retData = []
        for x in self.predictionData:
            subArr = []
            for y in x:
                subArr.append(self.normalizationFunction(y))
            retData.append(subArr)
        return retData

    

    def extractData(self):
        numpyX = np.zeros( ( len(self.x), len(self.x[0]), len(self.x[0][0]) ), dtype=np.int32 )
        numpyY = np.zeros( ( len(self.y), len(self.y[0]) ), dtype=np.int32 )
        for i in range(len(self.x)):
            for j in range(len(self.x[i])):
                for k in range(len(self.x[i][j])):
                    numpyX[i,j,k] = self.normalizationFunction(self.x[i][j][k])
        for i in range(len(self.y)):
            for j in range(len(self.y[i])):
                numpyY[i,j] = self.normalizationFunction(self.y[i][j])
        return [numpyX, numpyY]


def transformArray(arr, function):
    return [function(x) for x in arr]