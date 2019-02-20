'''
    :author: Colton Freitas
    :as-of: February 7th, 2019
'''

from AI.AbsAIModel import Abs_AIModel
from Common.Util.DateUtil import dateToTimestamp
from Data.Structures.CaselessDictionary import CaselessDictionary
from datetime import date
from typing import List
from os import path

class StoredModelFile:
    
    def __parseConfiguration(self):
        self.ModelID = self.modelConfiguration['General']['sModelID']
        self.Ticker = self.modelConfiguration['General']['sTicker']
        self.Epochs = self.modelConfiguration[self.ModelID]['iNumEpochs']

    def __init__ (self, filePathBase : str, modelConfiguration, load=False):
        self.modelConfiguration = modelConfiguration
        self.__parseConfiguration()
        self.FilePathBase = filePathBase
        if not load:
            self.__StoredModel = Abs_AIModel.createModelFromID(self.ModelID, modelConfiguration)

    def Evaluate(self):
        self.__StoredModel.Evaluate(self.modelConfiguration)

    def Train(self):
        self.__StoredModel.Train(self.modelConfiguration)

    @classmethod
    def parseConfigurationAdditions(cls, fileHandle, modelConfiguration):
        startingDate = float(fileHandle.readline())
        endingDate = float(fileHandle.readline())
        clusteredStocks = fileHandle.readline()
        iNumExamples = int(fileHandle.readline())

        line = fileHandle.readline()
        modelID = modelConfiguration['General']['sModelID']
        while not line.strip() == modelID:
            split = line.split('=')
            modelConfiguration[modelID][split[0]] = split[1]
            line = fileHandle.readline()

        if not len(clusteredStocks.strip()) == 0:
            split = clusteredStocks.strip().split(',')
            clusteredStocks = split
        else:
            clusteredStocks = []
        endingDate = date.fromtimestamp(endingDate)
        startingDate = date.fromtimestamp(startingDate)
        modelConfiguration['General']['dtStartingDate'] = startingDate
        modelConfiguration['General']['dtEndingDate'] = endingDate
        modelConfiguration['General']['lsClusteredStocks'] = clusteredStocks
        modelConfiguration['General']['iNumberDaysPerExample'] = iNumExamples

    @classmethod
    def Load(cls, filePath : str, modelConfiguration):
        filePathBase, fileName = path.split(filePath)
        fileHandle = open(filePath, 'r')
        cls.parseFileName(fileName, modelConfiguration)
        cls.parseConfigurationAdditions(fileHandle, modelConfiguration)
        ret = cls(filePathBase, modelConfiguration, load=True)
        ret.__StoredModel = Abs_AIModel.Load(fileHandle, modelConfiguration)
        fileHandle.close()
        return ret
        
    @classmethod
    def parseFileName(cls, fileName : str, modelConfiguration):
        split = fileName.split("_")
        modelConfiguration["General"]["sModelID"] = split[0]
        modelID = split[0]
        split = split[1].split("-")
        modelConfiguration["General"]["sTicker"] = split[0]
        modelConfiguration[modelID] = CaselessDictionary()
        modelConfiguration[modelID]["iNumEpochs"] = split[1]

    def Save(self):
        startingDate = self.modelConfiguration['General']['dtStartingDate']
        endingDate = self.modelConfiguration['General']['dtEndingDate']
        clusteredStocks = self.modelConfiguration['General']['lsClusteredStocks']

        endingDate = dateToTimestamp(endingDate)
        startingDate = dateToTimestamp(startingDate)
        clusteredStocks = ",".join(clusteredStocks)
        iNumExamples = self.modelConfiguration['General']['iNumberDaysPerExample']

        fileName = self.ModelID + '_' + self.Ticker + '-' + self.Epochs
        saveFile = open(self.FilePathBase.format(fileName), 'w')

        saveFile.write(str(startingDate) + '\n')
        saveFile.write(str(endingDate) + '\n')
        saveFile.write(clusteredStocks + '\n')
        saveFile.write(str(iNumExamples) + '\n')
        

        for key, value in self.modelConfiguration[self.ModelID].items():
            saveFile.write(key+'='+value+'\n')
        saveFile.write(self.ModelID + '\n')

        self.__StoredModel.Save(saveFile)

        saveFile.close()
