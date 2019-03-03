from Common.CommonValues import configurationFileLocation, stockTickerFileLocation, modelConfigurationFileLocation, modelConfiguration
from AI.SingleDataCategoryRNN import SingleDataCategoryRNN

from configparser import ConfigParser, NoSectionError, NoOptionError
from os import listdir
from os import path
from typing import List
import sys

def loginCredentialAssembling (password : str) -> List[str]:
    '''Assembles login credentials with the given password'''
    config = config_handling()
    config[2] = password
    return config

def getModelFiles(pathBase : str) -> List[str]:
    '''Returns a list of model files in the pathBase directory
    Does not return sub directories
    '''
    fileList = listdir(pathBase.format('.'))
    return [pathBase.format(x) for x in fileList if not path.isdir(pathBase.format(x))]

def write_default_configs(parser, file_position):
    '''Creates the default configuration file in file_position with default values
    :param parser: ConfigParser object to write default configuration with
    :param file_position: String containing the path of the file to write the configuration to

    '''
    
    parser.add_section('login_credentials')
    parser.set('login_credentials', 'user', 'root')
    parser.set('login_credentials', 'database', 'stock_testing')
    parser.set('login_credentials', 'host', 'localhost')
    fp = None
    try:
        fp = open(file_position, 'w')
    except FileNotFoundError:
        path.os.mkdir(path.split(file_position)[0])
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
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    except (NoSectionError, NoOptionError):
        write_default_configs(parser, configurationFileLocation)
        user = parser.get('login_credentials', 'user')
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    return [host, user, None, database]


def writeModelGeneral(parser):
    parser.add_section('General')
    parser.set('General', 'iMaxProcesses', '-1')
    parser.set('General', 'bEvaluationTraining', 'True')
    parser.set('General', 'iMaxTrainingTickers', '4')
    parser.set('General', 'fMinimumSimilarity', '.6')
    parser.set('General', 'iNumberDaysPerExample', '14')


def writeModelVMDSC(parser):
    parser.add_section('VMDSC')
    parser.set('VMDSC', 'iHiddenStateSize', '200')
    parser.set('VMDSC', 'iBackpropagationTruncationAmount', '5')
    parser.set('VMDSC', 'fLearningRate', '.1')
    parser.set('VMDSC', 'iLossEvalEpochs', '5')
    parser.set('VMDSC', 'sClusteringMethod', 'MD')
    parser.set('VMDSC', 'iNumEpochs', '1500')
    parser.set('VMDSC', 'iInputSize', '3')


def modelWriteDefaultConfigs(parser, filePosition: str):
    writeModelGeneral(parser)
    fp = None
    try:
        fp = open(filePosition, 'w')
    except FileNotFoundError:
        path.os.mkdir(path.split(filePosition)[0])
        fp = open(filePosition, 'w')
    parser.write(fp)
    fp.close()


def modelConfigHandling():
    '''Does all configuration handling using configparser package
    Uses file location that is build into this module,
    And it will write default values if the file is not found.
    '''
    parser = modelConfiguration
    try:
        fp = open(modelConfigurationFileLocation, 'r')
        fp.close()
    except FileNotFoundError:
        print("Model Configuration File not found: {0}\nPlease create a valid configuration file for model configuration.", file=sys.stderr)
        modelWriteDefaultConfigs(parser)
    configFile = open(modelConfigurationFileLocation, 'r')
    parser.read_file(configFile)
    configFile.close()

def get_stock_list():
    '''Obtains a list of all stock tickers to attempt to download
    
    '''
    file = open(stockTickerFileLocation, 'r')
    return_data = []
    for line in file:
        return_data.extend([line.strip()])
    file.close()
    return return_data