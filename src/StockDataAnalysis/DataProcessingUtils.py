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