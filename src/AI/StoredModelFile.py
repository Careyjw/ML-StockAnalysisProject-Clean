'''
    :author: Colton Freitas
    :as-of: February 7th, 2019
'''

from AI.AbsAIModel import Abs_AIModel
from Common.Util.DateUtil import dateToTimestamp
from typing import List

class StoredModelFile:
    
    def __parseConfiguration(self):
        self.ModelID = self.modelConfiguration['General']['sModelID']
        self.Ticker = self.modelConfiguration['General']['sTicker']
        self.Epochs = self.modelConfiguration[self.ModelID]['iNumEpochs']

    def __init__ (self, filePathBase : str, modelConfiguration):
        self.modelConfiguration = modelConfiguration
        self.__parseConfiguration()
        self.FilePathBase = filePathBase
        self.__StoredModel = Abs_AIModel.createModelFromID(self.ModelID, modelConfiguration)

    def Train(self):
        self.__StoredModel.Train(self.modelConfiguration)

    @classmethod
    def Load(cls, filePath : str, loginCredentials : List[str]):
        raise NotImplementedError()

    def __parseFileName(self, fileName : str):
        split = fileName.split("_")
        self.ModelID = split[0]
        split = fileName.split("-")
        self.Ticker = split[0]
        self.Epochs = split[1]

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
