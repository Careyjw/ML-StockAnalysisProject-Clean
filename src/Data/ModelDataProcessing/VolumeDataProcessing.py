from Data.ModelDataProcessing.DataProcessingUtils import DataProcessor, calculatePercentageChange
from SharedGeneralUtils.CommonValues import PercentageChangesSourceID, LimitedNumericChangeSourceID, MovementDirectionSourceID
from SharedGeneralUtils.SharedDataStorageClasses import TickerDataStorage, SourceDataStorage

def calcSign(x):
    '''Returns the sign of x
    :param x: Number like object to extract the sign from
    '''
    if (x < 0):
        return -1
    else:
        return 1

class VolumeDataProcessor:

    def __init__(self, loginCredentials):
        '''Data Manager Initialization

        '''
        self.dataManager = DataProcessor(loginCredentials)

    def close(self):
        self.dataManager.close()

    def __calcVolumeSignedDataForTicker(self, adj_closeData, open_closeData, volumeData, retVolumeData):
        '''Calculates and inserts signed volume data into retVolumeData
        :param adj_closeData: TickerDataStorage object holding the percentage change adjusted close values
        :type adj_closeData: TickerDataStorage
        :param open_closeData: TickerDataStorage object holding the raw opening price and adjusted close price values
        :type open_closeData: TickerDataStorage
        :param volumeData: TickerDataStorage object holding the raw volume_data and hist_date values
        :type volumeData: TickerDataStorage
        :param retVolumeData: TickerDataStorage object to store hist_date and signed volume_data in
        :type retVolumeData: TickerDataStorage
        '''
        
        for i in range(len(volumeData.data)):
            if (i == 0):
                openData = open_closeData.data[0][0]
                closingData = open_closeData.data[0][1]
                if (openData <= closingData):
                    retVolumeData.addData([volumeData.data[0][1], int(volumeData.data[0][0])])
                else:
                    retVolumeData.addData([volumeData.data[0][1], int(volumeData.data[0][0]) * -1])
            else:
                retVolumeData.addData([volumeData.data[i][1], int(volumeData.data[i][0]) * calcSign(adj_closeData.data[i-1][1]) ] )

    def generateVolumeUnsignedRawData(self, startDate=None, endDate=None):
        '''Retrieves the raw volumetric data from the database
        :param startDate: Starting date of the period to calculate changes with.
        :type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        :param endDate: Ending date of the period to calculate changes with.
        :type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        :return: List of TickerDataStorage objects containing data in the format [[day0, change0] ... [dayN, changeN]]
        '''
        
        volumeData = self.dataManager.getRawData(["hist_date", "volume_data"], startDate, endDate)
        for tickerData in volumeData:
            tickerData.data = [[x[0], int(x[1])] for x in tickerData.data]
        return volumeData

    def generateVolumeSignedRawData(self, startDate=None, endDate=None):
        '''Generates the raw signed representation of the volumetric data stored in the database
        :param startDate: Starting date of the period to calculate changes with.
        :type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        :param endDate: Ending date of the period to calculate changes with.
        :type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        :return: List of TickerDataStorage objects containing data in the format [[day0, change0] ... [dayN, changeN]]
        '''
        adj_closeData = self.dataManager.calculatePercentageChanges("adj_close", startDate, endDate).tickers
        open_closeData = self.dataManager.getRawData(["opening_price", "adj_close"])
        volumeData = self.dataManager.getRawData(["volume_data", "hist_date"], startDate, endDate)
        
        retVolumeData = [TickerDataStorage(x.ticker) for x in volumeData]

        for i in range(len(retVolumeData)):
            self.__calcVolumeSignedDataForTicker(adj_closeData[i], open_closeData[i], volumeData[i], retVolumeData[i])
        
        return retVolumeData

    def calculatePercentageChanges(self, startDate=None, endDate=None, signed=True):
        '''Calculates the Percentage Change for all stocks in database
        :param startDate: Starting date of the period to calculate changes with.
        :type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        :param endDate: Ending date of the period to calculate changes with.
        :type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        :return: SourceDataStorage object containing the returned data
        :storageFormat: 

        TickerDataStorage.data format: [ [date0, change0], [date1, change1] ... [dateN, changeN]]
        '''
        if (signed):
            volData = self.generateVolumeSignedRawData(startDate, endDate)
        else:
            volData = self.generateVolumeUnsignedRawData(startDate, endDate)
        retVolumeData = [TickerDataStorage(x.ticker) for x in volData]
        for i in range(len(volData)):
            dataStorage = volData[i]
            retDataStorage = retVolumeData[i]
            for j in range(1, len(dataStorage.data)):
                retDataStorage.addData([dataStorage.data[j][0],
                    calculatePercentageChange(dataStorage.data[j-1][1], dataStorage.data[j][1])])
        
        retSourceData = SourceDataStorage(PercentageChangesSourceID)
        for tickerStorage in retVolumeData:
            retSourceData.addTickerDataStorage(tickerStorage)
        
        return retSourceData
            

    def calculateLimitedNumericChange(self, startDate=None, endDate=None, signed=True):
        '''Calculates the Limited Numeric Change (defined below) for all stocks in database
        :param startDate: Starting date of the period to calculate changes with.
        :type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        :param endDate: Ending date of the period to calculate changes with.
        :type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        :return: SourceDataStorage object containing the returned data
        :storageFormat: 

        TickerDataStorage.data format: [ [date0, change0], [date1, change1] ... [dateN, changeN]]
        
        :define LimitedNumericChange: 
        
        If day 1 = 3.5 and day 2 = 3.0, 
        then the Limited Numeric Change between them is (3.0 - 3.5) / 3.5, or -.1428...
        If day 1 = 0 and day 2 > 0,
        then the Limited Numeric Change between them is 100%
        and day 2 < 0, then the Limited Numeric Change between them is -100%
        If day 1 = 0 and day 2 = 0,
        then the Limited Numeric Change between them is 0% (as expected, instead of an exception)
        '''
        volData = self.calculatePercentageChanges(startDate, endDate, signed)
        for tickerData in volData.tickers:
            for i in range(len(tickerData.data)):
                currentDayData = tickerData.data[i]

                if (currentDayData[1] < -100):
                    currentDayData[1] = -100
                elif (currentDayData[1] > 100):
                    currentDayData[1] = 100

                tickerData.data[i] = [currentDayData[0], round(currentDayData[1])]
        volData.sourceName = LimitedNumericChangeSourceID
        return volData
    
    def calculateMovementDirections(self, startDate=None, endDate=None, signed=True):
        '''Calculates the Movement Directions(defined below) for all stocks in database
        :param startDate: Starting date of the period to calculate changes with.
        :type startDate: datetime.datetime
        If None, then all dates until the ending date are used.
        :param endDate: Ending date of the period to calculate changes with.
        :type endDate: datetime.datetime
        If None, then all dates from the starting date until the most recent date 
        (in relation to the current time) stored in the database
        :return: SourceDataStorage object containing the returned data
        :storageFormat: 

        TickerDataStorage.data format: [ [date0, movement0], [date1, movement1] ... [dateN, movementN]]

        :define Movement Directions:
        
        
        if day 1 = x and day 2 ~= day 1,
        (where ~= is a tolerance of +-1%)
        then the Movement Direction is "stag"
        if day2 < day 1
        then the Movement Direction is "down"
        if day2 > day 1,
        then the Movement Direction is "up"
        '''        
        
        def getMovementPercentage(x):
            ''' Generates the movement percentage statement from the input
            :param x: Numerical percentage to base percentage string off of
            :rtype: String
            '''
            if (abs(x) <= 1):
                return "stag"
            if (x < 0):
                return "down"
            else: return "up"

        volData = self.calculateLimitedNumericChange(startDate, endDate, signed)
        for tickerData in volData.tickers:
            for i in range(len(tickerData.data)):
                currDayData = tickerData.data[i]
                tickerData.data[i] = [currDayData[0], getMovementPercentage(currDayData[1])]
        volData.sourceName = MovementDirectionSourceID
        return volData
        


    

