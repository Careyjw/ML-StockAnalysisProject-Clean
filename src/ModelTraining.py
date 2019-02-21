'''
:author: Colton Freitas
:as-of: February 7th, 2019
'''

from Training.ModelTrainingPipeline import ModelTrainingPipeline
from Training.TrainingFunctionStorage import trainModel

from Common.Util.ConfigurationUtils import insertAdditionalSettings, extractRelevantConfiguration

from Common.Util.CommonFunctions import config_handling, get_stock_list, modelConfigHandling

from configparser import ConfigParser

from argparse import ArgumentParser
from getpass import getpass

from os import cpu_count, path
from datetime import datetime, timedelta
from Common.CommonValues import modelStoragePathBase, evaluationModelStoragePathBase

def parseArgs():
    argParser = ArgumentParser(description="Module for training Recurrent Neural Networks on Volumetric data to predict stock price movements")
    argParser.add_argument('-modelID', dest='id', type=str, help="ID of the model to train", required=True)
    argParser.add_argument('-p', dest='p', type=str, help="Password of the database to use for login", default = "")
    namespace = argParser.parse_args()
    if (namespace.p == ""):
        namespace.p = getpass("Database Password:")

    return namespace

def verifyStoragePathsExist():
    if not path.exists(modelStoragePathBase.format('.')):
        path.os.mkdir(modelStoragePathBase.format('.'))
    if not path.exists(evaluationModelStoragePathBase.format('.')):
        path.os.mkdir(evaluationModelStoragePathBase.format('.'))
    
if __name__ == "__main__":
    namespace = parseArgs()

    login_creds = config_handling()
    login_creds[2] = namespace.p

    verifyStoragePathsExist()

    stockList = get_stock_list()

    modelConfigHandling()
    modelConfiguration = extractRelevantConfiguration(namespace.id)
    insertAdditionalSettings(modelConfiguration, login_creds, namespace.id)

    processCount = cpu_count() if int(modelConfiguration['General']['iMaxProcesses']) <= 0 else int(modelConfiguration['General']['iMaxProcesses'])

    pipeline = ModelTrainingPipeline(processCount, login_creds)

    pipeline.usePipeline(stockList, trainModel, modelConfiguration)


