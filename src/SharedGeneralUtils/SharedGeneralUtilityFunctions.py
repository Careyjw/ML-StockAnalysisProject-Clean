from configparser import ConfigParser, NoSectionError, NoOptionError
from os import listdir
from typing import List

from SharedGeneralUtils.ClientFilterTemplates import devClientFilter
from SharedGeneralUtils.CommonValues import startDate

from StockDataPrediction.TrainingFunctionStorage.TrainingFunctionStorage import combineDataSets, genTargetExampleSets, genTrainingExampleSets
from SharedGeneralUtils.CommonValues import modelStoragePathBase, VolumeMovementDirectionsSegmentedID, evalStartDate, VolumeLNCSegmentedID
from StockDataPrediction.MachineLearningModels.SingleDataCateogryRNN import SingleDataCategoryRNN
from StockDataPrediction.MachineLearningModels.TrainingDataStorages import RNNTrainingDataStorage
from StockDataPrediction.NormalizationFunctionStorage import movementDirectionDenormalization, movementDirectionNormalization

from EmailUtils.EClient import EClient, EClientFilter

from StockDataAnalysis.VolumeDataProcessing import VolumeDataProcessor
from StockDataAnalysis.DataProcessingUtils import DataProcessor
from StockDataAnalysis.ClusteringFunctionStorage import movingAverageClustering

from SharedGeneralUtils.CommonValues import configurationFileLocation, stockTickerFileLocation

from os import path

def genClients():
    '''Generates a quick list of clients to send data to.
    :status: temporary, will need to be replaced
    '''
    jimClient = EClient("Jim Carey", "careyjw@plu.edu", devClientFilter)
    coltonClient = EClient("Colton Freitas", "freitacr@plu.edu", devClientFilter)
    #return [jimClient, coltonClient]
    return [coltonClient]

def loadModel(fileExtension, modelFilePath):
    '''Loads model file from path
    '''
    #print(fileExtension)
    if fileExtension == 'scml':
        rnn = SingleDataCategoryRNN.load(modelFilePath)
        #print(rnn)
        return rnn

def genPredictionData(modelTypeName : str, ticker : str, loginCredentials : List[str], examplesPerSet : int, clusteringFunctionArgs : List):
    '''Generates prediction data based on the type of model loaded
    '''
    trainingTickers = None
    if modelTypeName == VolumeMovementDirectionsSegmentedID:
        trainingTickers = movingAverageClustering(ticker, loginCredentials, 0, clusteringFunctionArgs)
        trainingTickers = [trainingTickers[0]] + trainingTickers[1]
        
        dataProc = VolumeDataProcessor(loginCredentials)
        sourceStorages = dataProc.calculateMovementDirections(clusteringFunctionArgs[-1])
        dataStorage = [x.data for x in sourceStorages.tickers if x.ticker in trainingTickers]
        dataStorage = combineDataSets(dataStorage)
        predictionDataStorage = RNNTrainingDataStorage(movementDirectionNormalization, movementDirectionDenormalization)
        predictionDataStorage.addPredictionData(dataStorage[-examplesPerSet:])
        return predictionDataStorage
    elif modelTypeName == AdjestedMovementDirectionSegmentedID:
        pass

def genEvalData(modelTypeName : str, ticker : str, loginCredentials : List[str], examplesPerSet : int, clusteringFunctionArgs : List):
    '''Generates evaluation data for the given ticker and model type
    '''
    trainingTickers = None
    evalClusterArgs = clusteringFunctionArgs[:]
    #Sets the cluster period to be the start of the evaluation period, so the same stocks are selected for training
    #As when the evaluation model was trained.
    evalClusterArgs[-1] = evalStartDate
    if modelTypeName == VolumeMovementDirectionsSegmentedID:
        trainingTickers = movingAverageClustering(ticker, loginCredentials, 0, evalClusterArgs)
        trainingTickers = [trainingTickers[0]] + trainingTickers[1]

        dataProc = VolumeDataProcessor(loginCredentials)
        closeDataProc = DataProcessor(loginCredentials)
        sourceStorages = dataProc.calculateMovementDirections(clusteringFunctionArgs[-1])
        dataStorage = [x.data for x in sourceStorages.tickers if x.ticker in trainingTickers]
        dataStorage = combineDataSets(dataStorage)
        predData = genTrainingExampleSets(dataStorage, examplesPerSet)
    
        sourceStorages = closeDataProc.calculateMovementDirections("adj_close", clusteringFunctionArgs[-1])
        dataStorage = [x.data for x in sourceStorages.tickers if x.ticker == ticker][0]
        adj_closeTargetData = [x[1] for x in dataStorage]
        adj_closeTargetData = genTargetExampleSets(adj_closeTargetData, examplesPerSet)
        adj_closeTargetData = [[x[-1]] for x in adj_closeTargetData]
        dataStorage = RNNTrainingDataStorage(movementDirectionNormalization, movementDirectionDenormalization)
        
        dataProc.close()
        closeDataProc.close()

        return [predData, adj_closeTargetData, dataStorage]
    elif modelTypeName == VolumeLNCSegmentedID:
        #TODO Generate evaluation data for limited numeric change
        pass
    elif modelTypeName == AdjestedMovementDirectionSegmentedID:
        pass


def getModelFiles(pathBase : str) -> List[str]:
    '''Returns a list of model files in the pathBase directory
    Does not return sub directories
    '''
    fileList = listdir(pathBase.format('.'))
    return [pathBase.format(x) for x in fileList if not path.isdir(pathBase.format(x))]

def parseModelString(passedStr : str):
    '''Parses model filename string
    Assumes string is in format:
    "modelTypeName_ticker.extension"
    '''
    unScorePos = passedStr.find("_")
    periodPos = passedStr.find(".")
    modelTypeName = passedStr[:unScorePos]
    ticker = passedStr[unScorePos+1:periodPos]
    extension = passedStr[periodPos+1:]
    return [modelTypeName, ticker, extension]

def parseEvalModelString(passedStr : str) -> List[str]:
    '''Parses eval model filename string
    Assumes string is in the format:
    "modelTypeName_ticker-epochsTrained.extension"
    '''
    unScorePos = passedStr.find("_")
    periodPos = passedStr.find(".")
    dashPos = passedStr.find("-")
    modelTypeName = passedStr[:unScorePos]
    ticker = passedStr[unScorePos+1:dashPos]
    epochsTrained = passedStr[dashPos+1:periodPos]
    extension = passedStr[periodPos+1:]
    return [modelTypeName, ticker, epochsTrained, extension]

def write_default_configs(parser, file_position):
    '''Creates the default configuration file in file_position with default values
    :param parser: ConfigParser object to write default configuration with
    :param file_position: String containing the path of the file to write the configuration to

    '''
    
    parser.add_section('login_credentials')
    parser.set('login_credentials', 'user', 'root')
    parser.set('login_credentials', 'password', "")
    parser.set('login_credentials', 'database', 'stock_testing')
    parser.set('login_credentials', 'host', 'localhost')
    fp = open(file_position, 'w')
    parser.write(fp)
    fp.close()

def config_handling():
    '''Does all of the configuration handling using the configparser package
    This uses a file location hard-built into this module, namely configurationFileLocation
    This function has the ability to write said file as well with default values
    @return: List of login credentials
    @rtype: [String, String, String, String]
    '''
    parser = ConfigParser()
    try:
        fp = open(configurationFileLocation, 'r')
        fp.close()
    except FileNotFoundError:
        write_default_configs(parser, configurationFileLocation)
    config_file = open(configurationFileLocation, 'r')
    parser.read_file(config_file)
    config_file.close()
    try:
        user = parser.get('login_credentials', 'user')
        password = parser.get('login_credentials', 'password')
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    except (NoSectionError, NoOptionError):
        write_default_configs(parser, configurationFileLocation)
        user = parser.get('login_credentials', 'user')
        password = parser.get('login_credentials', 'password')
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    return [host, user, password, database]

def get_stock_list():
    '''Obtains a list of all stock tickers to attempt to download
    
    '''
    file = open(stockTickerFileLocation, 'r')
    return_data = []
    for line in file:
        return_data.extend([line.strip()])
    file.close()
    return return_data