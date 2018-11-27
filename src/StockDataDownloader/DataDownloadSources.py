'''
Created on Nov 27, 2018

@author: Colton Freitas
@summary: 

Contains the base methods for downloading data from the data sources
These methods will call further sub methods to accomplish their tasks
that are not needed to be visible for the calling method(s)
'''

from .YahooDataDownloader import getCookieAndCrumb, buildURL


def DownloadDataYahoo (tickerList):
    '''Downloads Stock Data from Yahoo
        @param tickerList: The list of stock tickers to obtain data for
        @type tickerList: Array of Strings
        @return Storage object containing obtained data
        @rtype: StockDataStorage
    '''
    
    cookie, crumb = getCookieAndCrumb()
    
    
    
    pass;
    
def DownloadDataGoogle (tickerList):
    '''Downloads Stock Data from Google
        @param tickerList: The list of stock tickers to obtain data for
        @type tickerList: Array of Strings
        @return Storage object containing obtained data
        @rtype: StockDataStorage
    '''    
    pass;