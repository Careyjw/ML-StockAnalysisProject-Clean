

class SourceDataStorage:
    
    def __init__(self, sourceName):
        '''Initializes the data storage object
            @param sourceName: Name of the source of the data
            @type sourceName: String
        '''
        self.sourceName = sourceName
        self.tickers = []
        
    def addTickerDataStorage(self, storage):
        '''Adds the TickerDataStorage object to the SourceDataStorage
            @param storage: Filled TickerDataStorage object
            @type storage: TickerDataStorage
        '''
        self.tickers.append(storage)

    def __str__(self):
        return str([self.sourceName, self.tickers])

    def __repr__(self):
        return self.__str__()
    
class TickerDataStorage:
    
    def __init__(self, ticker):
        '''Intializes the data storage object
            @param ticker: Stock ticker object stores data for
            @type ticker: String
        '''
        self.ticker = ticker
        self.data = []
        
    def addData(self, dataArray):
        '''Adds the supplied data to the storage
            @param dataArray: Data of the day being added
            @type dataArray: Array
            @format dataArray: [hist_date:datetime.datetime,
            high_price:float,
            low_price:float, 
            opening_price:float, 
            close_price:float, 
            adj_close:float, 
            volume_data:int]
        '''
        self.data.append(dataArray)

    def __str__(self):
        return "Data stored for ticker {}: {} entries".format(self.ticker, len(self.data))

    def __repr__(self):
        return self.__str__()
    