#imports
from Common.CommonValues import modelStoragePathBase
from Common.Util.CommonFunctions import getModelFiles
from Data.Structures.CaselessDictionary import CaselessDictionary
from AI.StoredModelFile import StoredModelFile
from typing import List
from Email.EMessageTemplates import devTickerPredEM
from Email.EMessage import EMessage

#methods
def LoadModel(loginCredentials:List[str]) -> List["StoredModelFile"]:
    ModelPaths=getModelFiles(modelStoragePathBase)
    models=[]
    for path in ModelPaths:
        modelConfiguration = CaselessDictionary()
        modelConfiguration['General'] = CaselessDictionary()
        modelConfiguration['General']['lsLoginCredentials'] = loginCredentials
        models.append(StoredModelFile.Load(path,modelConfiguration))
    return models

def predictModel(models:List["StoredModelFile"]) -> List[tuple]:
    predictions=[]
    for model in models:
        prediction=model.Predict()
        predictions.append((model,prediction))
    return predictions

def AssembleEmail(predictions: List[tuple]) -> "EMessage":
    baseString = "{modID} version of {ticker} trained for {epochs} epochs predicted value: {predicted}"
    NumTick=len(predictions)
    retTemplate=devTickerPredEM.multiplyKey("{ticker}",NumTick)
    for model,predicted in predictions:
        modPredString= baseString.format(ticker=model.Ticker, modID=model.ModelID, epochs=int(model.Epochs), predicted=predicted)
        retTemplate=retTemplate.replaceKey("{ticker}", modPredString)
    return retTemplate    

def PushEmails(clientList:List["EClient"],eMessage, emailSys):
    for client in ClientList:
        sendMsg = eMessage.replaceKey("{customer}",client.clientName)
        emailSys.sendMessage(sendMsg,client)

def Predict(loginCredentials, emailSys, clients):
    models = LoadModels(loginCredentials)
    Predictions= predictModel(models)
    template=AssembleEmail(Predictions)
    PushEmails(clients,template,emailSys)