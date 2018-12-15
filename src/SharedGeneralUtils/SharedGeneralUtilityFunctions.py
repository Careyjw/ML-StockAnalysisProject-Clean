from configparser import ConfigParser, NoSectionError, NoOptionError
from os import listdir
from typing import List

from SharedGeneralUtils.ClientFilterTemplates import devClientFilter
from SharedGeneralUtils.CommonValues import startDate

from StockDataPrediction.TrainingFunctionStorage.TrainingFunctionStorage import combineDataSets
from SharedGeneralUtils.CommonValues import modelStoragePathBase
from StockDataPrediction.MachineLearningModels.SingleDataCateogryRNN import SingleDataCategoryRNN
from StockDataPrediction.MachineLearningModels.TrainingDataStorages import RNNTrainingDataStorage
from StockDataPrediction.NormalizationFunctionStorage import movementDirectionDenormalization, movementDirectionNormalization

from EmailUtils.EClient import EClient, EClientFilter

from StockDataAnalysis.VolumeDataProcessing import VolumeDataProcessor
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
    if fileExtension == 'scml':
        rnn = SingleDataCategoryRNN.load(modelFilePath)
        return rnn

def genPredictionData(modelTypeName : str, ticker : str, loginCredentials : List[str], examplesPerSet : int):
    '''Generates prediction data based on the type of model loaded
    '''
    trainingTickers = None
    if modelTypeName == "VolMovDir":
        trainingTickers = movingAverageClustering(ticker, loginCredentials, 0, [.60, 5, 15, startDate])
        trainingTickers = [trainingTickers[0]] + trainingTickers[1]
        
        dataProc = VolumeDataProcessor(loginCredentials)
        sourceStorages = dataProc.calculateMovementDirections(startDate)
        dataStorage = [x.data for x in sourceStorages.tickers if x.ticker in trainingTickers]
        dataStorage = combineDataSets(dataStorage)
        predictionDataStorage = RNNTrainingDataStorage(movementDirectionNormalization, movementDirectionDenormalization)
        predictionDataStorage.addPredictionData(dataStorage[-examplesPerSet:])
        return predictionDataStorage

def getModelFiles() -> List[str]:
    '''Returns a list of model files in the modelStoragePathBase directory
    Does not return sub directories
    '''
    fileList = listdir(modelStoragePathBase.format('.'))
    return [modelStoragePathBase.format(x) for x in fileList if not path.isdir(x)]

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