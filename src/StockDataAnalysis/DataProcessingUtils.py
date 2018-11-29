'''
Created on Nov 27, 2018

@author: Colton Freitas

@summary: 

This file should contain classes and functions used to process data stored in the database
Into a usable format for machine learning training and clustering
'''
from DatabaseUtils.MySQLUtils import MYSQLDataManipulator


class DataProcessor:
    
    def __init__(self, login_credentials):
        '''
        
        @param login_credentials: List of credentials in format specified below
        @format login_credentials: [host, user, password, database (can be None)]
        '''
        
        self.dataManager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2], login_credentials[3])
        
    def calculateLimitedNumericChange(self, columnList, startDate=None, endDate=None):
        '''Calculates the Limited Numeric Change (defined below) for all stocks in database
        @param columnList: List of database table columns to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        
        @define LimitedNumericChange: 
        
        If day 1 = 3.5 and day 2 = 3.0, 
        then the Limited Numeric Change between them is (3.0 - 3.5) / 3.5, or -.1428...
        If day 1 = 0 and day 2 > 0,
        then the Limited Numeric Change between them is 100%
        and day 2 < 0, then the Limited Numeric Change between them is -100%
        If day 1 = 0 and day 2 = 0,
        then the Limited Numeric Change between them is 0% (as expected, instead of an exception)
        '''
        data = self.getRawData(columnList, startDate, endDate)
        pass
    
    def calculateMovementDirections(self, columnList, startDate=None, endDate=None):
        '''Calculates the Movement Directions(defined below) for all stocks in database
        @param columnList: List of database table columns to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        
        @define Movement Directions:
        
        
        if day 1 = x and day 2 ~= day 1,
        (where ~= is a tolerance of +-1%)
        then the Movement Direction is "stag"
        if day2 < day 1
        then the Movement Direction is "down"
        if day2 > day 1,
        then the Movement Direction is "up"
        '''
        data = self.getRawData(columnList, startDate, endDate)
        pass
    
    def getRawData(self, columnList, startDate=None, endDate=None):
        '''Obtains raw data for all tickers stored in the database
        @param columnList: List of database table columns to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        '''
        
        pass
    
    def genTrainingExamples(self, trainingDataList, targetDataList, numTrainingDataPerTargetData = 5):
        '''Takes list of training and target data and generate training examples to be used by machine learning models in this project
        
        :param trainingDataList: List of trainingData to generate training examples from
        :param targetDataList: List of target data to generate training examples from
        :param numTrainingDataPerTargetData: Number of training data values to be associated with one target value
        '''
        pass
    
class TrainingExampleStorage:
    def __init__(self):
        ''' Initialization of class variable
        
        '''
        self.data = []
        
    def addData(self, trainList, targetValue):
        ''' Adds singular training example to the contained data set
        
        :param trainList: List of training values that a model will use to predict the target value
        :param targetValue: Value that is "correct" for the provided list of training values
        '''
        pass