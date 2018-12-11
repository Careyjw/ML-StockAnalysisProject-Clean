from StockDataPrediction.MachineLearningModels.SingleDataCateogryRNN import RNNNormal, RNNTrainingDataStorage
from StockDataPrediction.ModelTrainingPipeline import TrainingGroup
from StockDataAnalysis.VolumeDataProcessing import VolumeDataProcessor
from StockDataAnalysis.DataProcessingUtils import DataProcessor
from StockDataPrediction.NormalizationFunctionStorage import movementDirectionDenormalization, movementDirectionNormalization
from typing import List

modelStoragePathBase = "../model_storage/{0}"

def parseParametersAndCreateRNN(trainingTickers : 'TrainingGroup', trainingFunctionArgs : List):
    primaryTicker = trainingTickers.primaryTicker
    otherTickers = trainingTickers.trainingTickers
    
    startingDataDate = trainingFunctionArgs[0]

    hiddenStateSize, backpropogationTruncationAmount, learningRate, evalLossAfter = trainingFunctionArgs[1]
    
    numTrainingEpochs = trainingFunctionArgs[2]

    rnn = RNNNormal(hiddenStateSize, 3, len(otherTickers) + 1, backpropogationTruncationAmount, learningRate, evalLossAfter)

    trainTickers = otherTickers + [primaryTicker]

    examplesPerSet = trainingFunctionArgs[3]

    return [rnn, trainTickers, startingDataDate, numTrainingEpochs, examplesPerSet]

def combineDataSets(dataSets : List[List]):
    nonDatedData = []
    for dataSet in dataSets:
        nonDatedData.append( [x[1] for x in dataSet] )

    retData = []
    for i in range(len(nonDatedData[0])):
        retData.append([])

    for i in range(len(retData)):
        for dataSet in nonDatedData:
            retData[i].append(dataSet[i])

    return retData

def genTargetExamples(targetDataSet : List, examplesPerSet : int):
    retlist = []
    numExamplesGenerated = len(targetDataSet) - examplesPerSet
    for i in range(numExamplesGenerated):
        shiftedIndex = i+1
        retlist.append( targetDataSet[ shiftedIndex:shiftedIndex + examplesPerSet ] )
    return retlist

def genTrainExamples(trainDataSet : List[List], examplesPerSet : int):
    retlist = []
    numExamplesGenerated = len(trainDataSet) - examplesPerSet
    for i in range(numExamplesGenerated):
        retlist.append( trainDataSet[ i:i+examplesPerSet] )

    return retlist

def trainVolumeRNNMovementDirections(trainingTickers : 'TrainingGroup', trainingFunctionArgs : List, loginCredentials : List[str]):
    '''Trains RNN models using volumetric data
    :trainingFunctionArgs format:
    [startDate : datetime, (hiddenStateSize : int, backpropogationTruncationAmount : int, learningRate : float, evalLossAfter : int), numTrainingEpochs : int, examplesPerSet : int]
    '''

    rnn, trainTickers, startDate, numEpochs, examplesPerSet = parseParametersAndCreateRNN(trainingTickers, trainingFunctionArgs)

    dataProc = VolumeDataProcessor(loginCredentials)
    closeDataProc = DataProcessor(loginCredentials)

    sourceStorages = dataProc.calculateMovementDirections(startDate)
    
    dataStorage = [x.data for x in sourceStorages.tickers if x.ticker in trainTickers]
    
    preExemplifiedTrainingData = combineDataSets(dataStorage)

    sourceStorages = closeDataProc.calculateMovementDirections("adj_close", startDate)
    dataStorage = [x.data for x in sourceStorages.tickers if x.ticker == trainingTickers.primaryTicker][0]
    adj_closeTargetData = [x[1] for x in dataStorage]

    adj_closeTargetData = genTargetExamples(adj_closeTargetData, examplesPerSet)
    trainingData = genTrainExamples(preExemplifiedTrainingData, examplesPerSet)

    trainingDataStorage = RNNTrainingDataStorage(movementDirectionNormalization, movementDirectionDenormalization)
    for i in range(len(trainingData)):
        trainingDataStorage.addTrainingExample(trainingData[i], adj_closeTargetData[i])

    rnn.trainEpoch_BatchGradientDescent(trainingDataStorage, numEpochs)
    rnn.store(modelStoragePathBase.format(
        "VolMovDir_{0}.scml".format(trainingTickers.primaryTicker)
    ))
    dataProc.close()
    closeDataProc.close()
