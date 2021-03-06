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
        '''Adds the training example to the storage
        '''
        self.x.append(x)
        self.y.append(y)

    def addPredictionData(self, x : List[List]):
        '''Sets the prediction data to the supplied list
        '''
        self.predictionData.append(x)

    def extractPredictionData(self):
        '''Extracts Prediction Data from storage, applying the normalization function before returning
        '''
        retData = []
        predData = self.predictionData[0]
        for x in predData:
            subArr = []
            for y in x:
                subArr.append(self.normalizationFunction(y))
            retData.append(subArr)
        self.predictionData = self.predictionData[1:]
        return retData

    def extractData(self):
        '''Exracts Training Data from storage, applying the normalization function before returning
        '''
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
    '''Applies the function to all values in the array
    '''
    return [function(x) for x in arr]