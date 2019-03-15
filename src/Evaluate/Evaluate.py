from AI.StoredModelFile import StoredModelFile
from Email.EMessageTemplates import devTickerEvalEM
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

def AssembleEmailTemplate(accuracyList : List[tuple]) -> "EMessage":
    baseModelAccuracyString = "{modID} version of {ticker} trained for {epochs} epochs accuracy : {accuracy}"
    iNumTickers = len(accuracyList)
    retTemplate = devTickerEvalEM.multiplyKey("{ticker}", iNumTickers)
    for model, accuracy in accuracyList:
        modAccuracyString = baseModelAccuracyString.format(ticker=model.Ticker, modID=model.ModelID, epochs=int(model.Epochs), accuracy=accuracy)
        retTemplate = retTemplate.replaceKey("{ticker}", modAccuracyString)
    return retTemplate

def PushEmails(clientList : List["EClient"], eMessage, emailSys):
    for cli in clientList:
        sendMsg = eMessage.replaceKey("{customer}", cli.clientName)
        emailSys.sendMessage(sendMsg, cli)

def Evaluate(loginCredentials, emailSystem, clients, printOutputToScreen):
    models = LoadModels(loginCredentials)
    accList = EvaluateModels(models)
    template = AssembleEmailTemplate(accList)
    if not printOutputToScreen:
        PushEmails(clients, template, emailSystem)
    else:
        print(template)

