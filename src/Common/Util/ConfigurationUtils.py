from Data.Structures.CaselessDictionary import CaselessDictionary
from SharedGeneralUtils.CommonValues import startDate, evalStartDate, modelConfiguration
from datetime import timedelta

def extractRelevantConfiguration(modelID):
    modelDict = CaselessDictionary()
    for x in modelConfiguration.items():
        if (x[0] == modelID or x[0] == 'General'):
            #x[1] is now a section, but this is still not nicely mutable
            modelDict[x[0]] = CaselessDictionary()
            for xi in x[1].items():
                modelDict[x[0]][xi[0]] = xi[1]
    return modelDict

def insertStartingDate(modelConfiguration):
    startingDate = startDate
    endingDate = startDate + timedelta(365)
    if modelConfiguration['General']['bEvaluationTraining'] == 'True':
        startingDate = evalStartDate
        endingDate = startDate
    modelConfiguration['General']['dtStartingDate'] = startingDate
    modelConfiguration['General']['dtEndingDate'] = endingDate
    

def insertLoginCredentials(modelConfiguration, loginCredentials):
    modelConfiguration['General']['lsLoginCredentials'] = loginCredentials

def insertAdditionalSettings(modelConfiguration, loginCredentials, modelID):
    modelConfiguration['General']['sModelID'] = modelID
    insertStartingDate(modelConfiguration)
    insertLoginCredentials(modelConfiguration, loginCredentials)

def insertTicker(modelConfiguration, ticker):
    modelConfiguration['General']['sTicker'] = ticker

def insertClusteredStocks(modelConfiguration, clusteredStocks):
    modelConfiguration['General']['lsClusteredStocks'] = clusteredStocks