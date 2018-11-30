import unittest
from StockDataPrediction.ModelTrainingPipeline import ModelTrainingPipeline
from SharedGeneralUtils.SharedGeneralUtils import config_handling
from time import sleep

def NormalClusteringFunction (primaryTicker, loginCredentials, trainingPosition):
    sleep(5)
    return [primaryTicker, [primaryTicker] * 5, trainingPosition]

def NormalTrainingFunction (trainingTickers, trainingFunctionArgs, loginCredentials):
    sleep(10)
    return trainingTickers.primaryTicker

def BrutalTrainingFunction (trainingTickers, trainingunctionArgs, loginCredentials):
    sleep(10)
    return trainingTickers.primaryTicker

def BrutalClusteringFunction(primaryTicker, loginCredentials, trainingPosition):
    sleep(5)
    return [pimaryTicker, [primaryTicker], trainingPosition]  * 5

class ModelTrainingPipelineTest (unittest.TestCase):

    def setUp(self):
        self.pipeline = ModelTrainingPipeline(8, config_handling())

    def testPipelineNormalFunctions(self):
        ''' Just does a test of the basic workflow of the pipeline
        Shouldn't try and press any edge cases, just use two custom functions
        that are used in the usePipeline function
        '''
        returnedValues = self.pipeline.usePipeline(["AAPL", "F", "MCD"], NormalTrainingFunction, [True, True, True], NormalClusteringFunction)
        self.assertTrue("AAPL" in returnedValues)
        self.assertTrue("F" in returnedValues)
        self.assertTrue("MCD" in returnedValues)

    