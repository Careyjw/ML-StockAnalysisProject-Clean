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
    def createModelFromID(cls, ID : str, modelConfiguration):
        if (ID.endswith('SC')):
            return cls.registeredModels['SC'](modelConfiguration)

    @abstractmethod
    def Train(self, modelConfiguration):
        pass
    
    @abstractmethod
    def Predict(self, modelConfiguration):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def Load(cls, fileHandle):
        #TODO: Create basic implementation to load models
        raise NotImplementedError

    @abstractmethod
    def Save(self, fileHandle):
        pass

    @abstractmethod
    def Evaluate(self, modelConfiguration):
        raise NotImplementedError