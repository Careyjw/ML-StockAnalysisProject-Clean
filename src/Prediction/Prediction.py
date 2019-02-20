#imports
from Common.CommonValues import modelStoragePathBase
from Common.Util.CommonFunctions import getModelFiles
from Data.Structures.CaselessDictionary import CaselessDictionary
from AI.StoredModelFile import StoredModelFile

#methods
def LoadModel(loginCredentials:List[str]) -> List["StoredModelFile"]:
    ModelPaths=getModelFiles(modelStoragePathBase)
    models=[]
    for path in ModelPaths:
        modelConfiguration = caselessDictionary()
        modelConfiguration['General'] = CaselessDictionary()
        modelConfiguration['General']['lsLoginCredentials'] = loginCredentials
        models.append(StoredModelFile.Load(path,modelConfiguration))
    return models
def predict(models:List["StoredModelFile"]) -> List[tuple]:
    
#template

#pushEmail