from AI.StoredModelFile import StoredModelFile
from Common.CommonValues import evaluationModelStoragePathBase
from Common.Util.CommonFunctions import getModelFiles
from typing import List


def LoadModels(loginCredentials : List[str]) -> List["StoredModelFile"]:
    evalModelFilePaths = getModelFiles(evaluationModelStoragePathBase)
    storedModels = []
    for path in evalModelFilePaths:
        storedModels.append(StoredModelFile.Load(path))
    return storedModels