from AI.StoredModelFile import StoredModelFile
from Email.EMessageTemplates import devTickerPredEM
from Email.EMessage import EMessage
from Common.CommonValues import evaluationModelStoragePathBase
from Common.Util.CommonFunctions import getModelFiles
from Data.Structures.CaselessDictionary import CaselessDictionary
from typing import List


def LoadModels(loginCredentials : List[str]) -> List["StoredModelFile"]:
    evalModelFilePaths = getModelFiles(evaluationModelStoragePathBase)
    storedModels = []
    for path in evalModelFilePaths:
        modelConfiguration = CaselessDictionary()
        modelConfiguration['General'] = CaselessDictionary()
        modelConfiguration['General']['lsLoginCredentials'] = loginCredentials
        storedModels.append(StoredModelFile.Load(path, modelConfiguration))
    return storedModels

def EvaluateModels(loadedModels : List["StoredModelFile"]) -> List[tuple]:
    accuracies = []
    for model in loadedModels:
        accuracy = model.Evaluate()
        accuracies.append( (model, accuracy) )
    return accuracies

