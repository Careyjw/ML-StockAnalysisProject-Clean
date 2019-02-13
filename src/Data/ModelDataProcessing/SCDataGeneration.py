'''
:author: Colton Freitas
:as-of: February 9th, 2019
Holds data retrieval/generation functions for Single Data Category Models
'''

from Data.Structures.ClusteredStockStorage import ClusteredStockStorage
from Data.Structures.TrainingDataStorages import RNNTrainingDataStorage
from Data.ModelDataProcessing.VolumeDataProcessing import VolumeDataProcessor
from Data.ModelDataProcessing.DataProcessingUtils import DataProcessor

from Training.TrainingUtilityFunctions import genTargetExampleSets, genTrainingExampleSets, combineDataSets
from Training.NormalizationFunctionStorage import movementDirectionDenormalization, movementDirectionNormalization
from Training.NormalizationFunctionStorage import limitedNumericChangeDenormalization, limitedNumericChangeNormalization

from datetime import timedelta



def translateDataRetrievalMethod(modelID : str):
    '''Returns the method that will perform data retrieval for a Single Data Category Model
    Will also return extra arguments that will be needed to run the method'''
    if (modelID == "VMDSC"):
        args = {}
        args['targetCategory'] = 'adj_close'
        args['dataProcessingMethod'] = 'MD'
        args['normalizationFunction'] = movementDirectionNormalization
        args['denormalizationFunction'] = movementDirectionDenormalization
        argHelper = SDCDataRetrievalArgumentHelper(args)
        return [volumeCategoryDataRetrieval, argHelper]

def useSpecializedDataProcessor(processingMethodID : str, dataProcessingObject, startDate, endDate):
    if (processingMethodID == "MD"):
        return dataProcessingObject.calculateMovementDirections(startDate, endDate=endDate)
    elif (processingMethodID == "LNC"):
        return dataProcessingObject.calculateLimitedNumericChange(startDate, endDate=endDate)

def useGeneralDataProcessor(processingMethodID : str, dataProcessingObject, startDate, endDate, targetedColumn):
    if (processingMethodID == "MD"):
        return dataProcessingObject.calculateMovementDirections(targetedColumn, startDate, endDate=endDate)
    elif (processingMethodID == "LNC"):
        return dataProcessingObject.calculateLimitedNumericChange(targetedColumn, startDate, endDate=endDate)

def produceTargetExampleSets(sourceDataStorage, examplesPerSet, trainingTickers):
    dataStorages = [x.data for x in sourceDataStorage.tickers if x.ticker == trainingTickers[-1]][0]
    targetData = [x[1] for x in dataStorages]
    return genTargetExampleSets(targetData, examplesPerSet)

def produceTrainingExampleSets(sourceDataStorage, examplesPerSet, trainingTickers):
    dataStorages = [x.data for x in sourceDataStorage.tickers if x.ticker in trainingTickers]
    dataStorages = combineDataSets(dataStorages)
    return genTrainingExampleSets(dataStorages, examplesPerSet)

def fillTrainingDataStorage(storage, trainingData, targetData):
    for i in range(len(trainingData)):
        storage.addTrainingExample(trainingData[i], targetData[i])

def volumeCategoryDataRetrieval(argHelper : 'SDCDataRetrievalArgumentHelper'):
    args = argHelper.args
    startDate = args['startDate']
    endDate = startDate + timedelta(365)
    trainingTickers = args['clusteredStockStorage'].getTrainingTickers()

    volDataProcessor = VolumeDataProcessor(args['loginCredentials'])
    targetDataProcessor = DataProcessor(args['loginCredentials'])
    
    sourceDataStorages = useSpecializedDataProcessor(args['dataProcessingMethod'], volDataProcessor, startDate, endDate)
    trainingData = produceTrainingExampleSets(sourceDataStorages, args['numExamples'], trainingTickers)
    volDataProcessor.close()

    sourceDataStorages = useGeneralDataProcessor(args['dataProcessingMethod'], targetDataProcessor, startDate, endDate, args['targetCategory'])
    targetData = produceTargetExampleSets(sourceDataStorages, args['numExamples'], trainingTickers)
    
    trainingDataStorage = RNNTrainingDataStorage(args['normalizationFunction'], args['denormalizationFunction'])
    fillTrainingDataStorage(trainingDataStorage, trainingData, targetData)
    return trainingDataStorage
    
    


class SDCDataRetrievalArgumentHelper:

    def __init__(self, currArgs):
        self.args = currArgs

    def __coallateClusteredStocks(self, modelConfiguration):
        clusteredStocks = modelConfiguration['General']['lsClusteredStocks']
        ticker = modelConfiguration['General']['sTicker']

        ret = ClusteredStockStorage(ticker)
        for x in clusteredStocks:
            ret.addTicker(x)
        return ret

    def fillFromModelConfiguration(self, modelConfiguration):
        startDate = modelConfiguration['General']['dtStartingDate']
        loginCredentials = modelConfiguration['General']['lsLoginCredentials']
        iNumExamples = int(modelConfiguration['General']['iNumberDaysPerExample'])

        self.args['startDate'] = startDate
        self.args['loginCredentials'] = loginCredentials
        self.args['clusteredStockStorage'] = self.__coallateClusteredStocks(modelConfiguration) 
        self.args['numExamples'] = iNumExamples

    def addStartDate(self, startDate):
        self.args['startDate'] = startDate
    
    def addLoginCredentials(self, loginCredentials):
        self.args['loginCredentials'] = loginCredentials
    
    def addClusteredStocks(self, clusteredStockStorage):
        self.args['clusteredStockStorage'] = clusteredStockStorage

    def addNumberOfExamples(self, iNumExamplesPerSet):
        self.args['numExamples'] = iNumExamplesPerSet

    