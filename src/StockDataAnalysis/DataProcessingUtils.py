'''
Created on Nov 27, 2018

@author: Colton Freitas

@summary: 

This file should contain classes and functions used to process data stored in the database
Into a usable format for machine learning training and clustering
'''
from DatabaseUtils.MySQLUtils import MYSQLDataManipulator, stockListTableColList, tableNameBaseString
from SharedGeneralUtils.SharedDataStorageClasses import SourceDataStorage, TickerDataStorage
from datetime import datetime as dt

LimitedNumericChangeSourceID = "LimitedNumericChangeCalculator"
MovementDirectionSourceID = "MovementDirectionCalculator"
PercentageChangesSourceID = "PercentageChangesCalculator"

class DataProcessor:
    
    def __init__(self, login_credentials):
        '''
        
        @param login_credentials: List of credentials in format specified below
        @format login_credentials: [host, user, password, database (can be None)]
        '''
        
        self.dataManager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2], login_credentials[3])

    def close(self):
        self.dataManager.close()
        
    def calculatePercentageChanges(self, column, startDate = None, endDate = None):
        '''Calculates the Limited Numeric Change (defined below) for all stocks in database
        @param column: Name of database table column to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        @type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        @type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        @storageFormat: 

        TickerDataStorage.data format: [ [date0, change0], [date1, change1] ... [dateN, changeN]]
        
        @define LimitedNumericChange: 
        
        If day 1 = 3.5 and day 2 = 3.0, 
        then the Limited Numeric Change between them is (3.0 - 3.5) / 3.5, or -.1428...
        If day 1 = 0 and day 2 > 0,
        then the Limited Numeric Change between them is 100%
        and day 2 < 0, then the Limited Numeric Change between them is -100%
        If day 1 = 0 and day 2 = 0,
        then the Limited Numeric Change between them is 0% (as expected, instead of an exception)
        '''
        colList = ['hist_date']
        colList.append(column)
        
        retDataStorage = SourceDataStorage(PercentageChangesSourceID)


        data = self.getRawData(colList, startDate, endDate)
        for tickerDataStorage in data:
            lncTickerData = TickerDataStorage(tickerDataStorage.ticker)
            for i in range(len(tickerDataStorage.data[1:])):
                lncDate = tickerDataStorage.data[i+1][0]
                prevDateData = tickerDataStorage.data[i][1]
                currDateData = tickerDataStorage.data[i+1][1]
                lncTickerData.addData([lncDate, calculatePercentageChange(prevDateData, currDateData)])
            retDataStorage.addTickerDataStorage(lncTickerData)
        
        return retDataStorage

    def calculateLimitedNumericChange(self, column, startDate=None, endDate=None):
        '''Calculates the Limited Numeric Change (defined below) for all stocks in database
        @param column: Name of database table column to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        @type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        @type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        @storageFormat: 

        TickerDataStorage.data format: [ [date0, change0], [date1, change1] ... [dateN, changeN]]
        
        @define LimitedNumericChange: 
        
        If day 1 = 3.5 and day 2 = 3.0, 
        then the Limited Numeric Change between them is (3.0 - 3.5) / 3.5, or -.1428...
        If day 1 = 0 and day 2 > 0,
        then the Limited Numeric Change between them is 100%
        and day 2 < 0, then the Limited Numeric Change between them is -100%
        If day 1 = 0 and day 2 = 0,
        then the Limited Numeric Change between them is 0% (as expected, instead of an exception)
        '''
        retDataSource = self.calculatePercentageChanges(column, startDate, endDate)

        for tickerData in retDataSource.tickers:
            for i in range(len(tickerData.data)):
                currDayData = tickerData.data[i]
                tickerData.data[i] = [currDayData[0], round(currDayData[1])]
        retDataSource.sourceName = LimitedNumericChangeSourceID

        
        return retDataSource
    
    def calculateMovementDirections(self, column, startDate=None, endDate=None):
        '''Calculates the Movement Directions(defined below) for all stocks in database
        @param column: Name of database table column to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        @type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        @type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: SourceDataStorage object containing the returned data
        @storageFormat: 

        TickerDataStorage.data format: [ [date0, movement0], [date1, movement1] ... [dateN, movementN]]

        @define Movement Directions:
        
        
        if day 1 = x and day 2 ~= day 1,
        (where ~= is a tolerance of +-1%)
        then the Movement Direction is "stag"
        if day2 < day 1
        then the Movement Direction is "down"
        if day2 > day 1,
        then the Movement Direction is "up"
        '''

        def getMovementPercentage(x):
            if (abs(x) <= 1):
                return "stag"
            if (x < 0):
                return "down"
            else: return "up"
        
        retDataSource = self.calculateLimitedNumericChange(column, startDate, endDate)
        
        for tickerData in retDataSource.tickers:
            for i in range(len(tickerData.data)):
                currDayData = tickerData.data[i]
                tickerData.data[i] = [currDayData[0], getMovementPercentage(currDayData[1])]
        retDataSource.sourceName = MovementDirectionSourceID

        return retDataSource

    def __getStoredTickersAndStoredSources(self):
        '''Searches Database and Returns a list of tickers that have data
        @return: List of SourceDataStorage objects,
            which contain lists of TickerDataStorage objects without data, but with tickers
        '''

        storedTickers = self.dataManager.select_from_table("stock_list", stockListTableColList)
        val = []
        for ticker in storedTickers:
            for i in range(len(ticker[1:])):
                if (ticker[1:][i]):
                    val.append( (ticker[0], stockListTableColList[i+1]) )
                    break
        storedTickers = val

        ret = []

        for source in stockListTableColList[1:]:
            dataStorage = SourceDataStorage(source)
            for ticker, dataSource in storedTickers:
                if (dataSource == source):
                    dataStorage.addTickerDataStorage(TickerDataStorage(ticker))
            ret.append(dataStorage)

        return ret

    
    def getRawData(self, columnList, startDate=None, endDate=None) -> list:
        '''Obtains raw data for all tickers stored in the database
        @param columnList: List of database table columns to extract data from.
        @param startDate: Starting date of the period to calculate changes with.
        @type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        @param endDate: Ending date of the period to calculate changes with.
        @type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        @return: list of TickerDataStorage objects containing the data returned
        '''
        
        startingDate = startDate
        endingDate = endDate

        if (startDate == None):
            startingDate = dt.utcfromtimestamp(0.0)
        if (endDate == None):
            endingDate = dt.now()

        startingDate = startingDate.strftime("%Y-%m-%d")
        endingDate = endingDate.strftime("%Y-%m-%d")

        conditionalString = 'where hist_date <= Date("{}") and hist_date >= Date("{}") order by hist_date'
        conditionalString = conditionalString.format(endingDate, startingDate)

        ret = []
        
        storedTickers = self.__getStoredTickersAndStoredSources()
        for sourceData in storedTickers:
            sourceString = sourceData.sourceName
            for tickerData in sourceData.tickers:
                tickerString = tickerData.ticker
                storedData = self.dataManager.select_from_table(tableNameBaseString.format(tickerString, sourceString), columnList, conditional = conditionalString)
                for dataSet in storedData:
                    tickerData.addData(dataSet)
                ret.append(tickerData)
        
        return ret
    
    def genTrainingExamples(self, trainingDataList, targetDataList, numTrainingDataPerTargetData = 5):
        '''Takes list of training and target data and generate training examples to be used by machine learning models in this project
        
        :param trainingDataList: List of trainingData to generate training examples from
        :param targetDataList: List of target data to generate training examples from
        :param numTrainingDataPerTargetData: Number of training data values to be associated with one target value
        :raise ValueError: If numTrainingDataPerTargetData <= 0
        '''
        if (numTrainingDataPerTargetData <= 0):
            raise ValueError("Number of training data must be greater than 0: {}".format(numTrainingDataPerTargetData))
        
        trainingPerTarget = numTrainingDataPerTargetData-1

        retExampleStorage = TrainingExampleStorage()

        for i in range(len(trainingDataList[trainingPerTarget:])):
            trainingData = trainingDataList[i]
            targetData = targetDataList[i]
            retExampleStorage.addData(trainingData, targetData)

        return retExampleStorage

    def createTrainingDataList(self, data, numTrainingDataPerTargetData = 5):
        '''Takes a list of data and transforms it into a list usable in genTrainingExamples
        :param data: List of data to transform
        :param numTrainingDataPerTargetData: Number of training data values to be associated with one target value
        :return: List usable by genTrainingExamples
        '''
        retList = []
        for i in range(len(data[numTrainingDataPerTargetData:])):
            retList.append(data[i:i+numTrainingDataPerTargetData])
        return retList
    
    def createTargetDataList(self, data, numTrainingDataPerTargetData=5):
        '''Takes a list of data and transforms it into a list usable in genTrainingExamples
        :param data: List of data to transform
        :param numTrainingDataPerTargetData: Number of training data values to be associated with one target value
        :return: List usable by genTrainingExamples
        '''
        return data[numTrainingDataPerTargetData:]
    
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
        self.data.append([trainList, targetValue])

    def getX(self):
        '''Returns a list of the training data contained in this object
        '''
        return [x[0] for x in self.data]
    def getY(self):
        '''Returns a list of the target data contained in this object
        '''
        return [y[1] for y in self.data]
    

def calculatePercentageChange(x, y):
    '''Calculates the percentage change between x and y
    @type x: float
    @type y: float
    :NOTE:

    This function uses special logic for when one or both of the parameters are zero
    These cases are handled accordingly:
    if x == y == 0:
        return 0
    if x == 0 and not y == 0:
        return 100
    if not x == 0 and y == 0:
        return -100
    '''
    if (x == 0 and y == 0):
        return 0
    elif (x == 0 and not y == 0):
        return 100
    elif (not x == 0 and y == 0):
        return -100
    else:
        return ((y - x) / x) * 100
