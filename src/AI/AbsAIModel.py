'''
    :author: Colton Freitas
    :as-of: February 7th, 2019
'''

from configparser import ConfigParser
from abc import abstractmethod

class Abs_AIModel:

    registeredModels = {}

    @classmethod
    def registerModel(cls, modelStr, model):
        cls.registeredModels[modelStr] = model

    @classmethod
    def getModelTypeFromID(cls, ID : str):
        for endingString, model in cls.registeredModels.items():
            if (ID.endswith(endingString)):
                return model

    @classmethod
    def createModelFromID(cls, ID : str, modelConfiguration):
        return cls.getModelTypeFromID(ID)(modelConfiguration)

    @abstractmethod
    def Train(self, modelConfiguration):
        pass
    
    @abstractmethod
    def Predict(self, modelConfiguration):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def Load(cls, fileHandle, modelConfiguration):
        pass

    @abstractmethod
    def Save(self, fileHandle):
        pass

    @abstractmethod
    def Evaluate(self, modelConfiguration):
        raise NotImplementedError