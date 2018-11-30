'''
Created on Nov 27, 2018

@author: Colton Freitas
@summary: 

Contains functions shared between downloading methods
'''

import urllib.request as ureq
from urllib.error import HTTPError

def openURL(url, cookie = None):
    '''Opens the URL specified with basic error reporting
        @param url: The url to connect to
        @type url: String
        @param cookie: A cookie to place in the HTTP headers (optional)
        @type cookie: String
        @return: 
        
        Array of two elements:
            Element one is whether the connection was successful
            Element two is either the HTTP object (if successful) or the error code or exception if not successful.
        @rtype: [bool, HTTPConnection] or [bool, int] or [bool, HTTPError]
    '''
    opener = ureq.build_opener()
    if not cookie == None:
        opener.addheaders.append( ('Cookie', cookie))
    hres = None
    try:
        hres = opener.open(url)
    except HTTPError as e:
        return [False, (e)]
    if not str(hres.getcode())[0] == '2':
        return [False, hres.getcode()]
    else:
        return [True, hres]
    
    
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
        return "Data stored for ticker {}".format(self.ticker)

    def __repr__(self):
        return str([self.ticker, self.data])
    