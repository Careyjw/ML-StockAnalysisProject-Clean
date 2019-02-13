'''
Created on Nov 27, 2018

@author: Colton Freitas
@summary: 

Contains specialized methods to download stock data from Yahoo
'''

from StockDataDownloader.SharedUtilities import openURL
from datetime import datetime as dt
from SharedGeneralUtils.SharedDataStorageClasses import TickerDataStorage

crumbURL = 'https://finance.yahoo.com/quote/AAPL?p=AAPL'
baseURL = 'https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}'

def getCookieAndCrumb():
    '''Obtains a cookie and crumb from the Yahoo servers
       
       @raise ValueError:
       
       Raises a Value Error if the connection to crumbURL fails
       This failure is defined as the HTTP response being anything other than 2xx
       
       @return: [cookie, crumb]
       @rtype: [String, String]
    '''
    
    stat = openURL(crumbURL)
    if not stat[0]:
        if type(stat[1]) == type(3):
            raise ValueError("Connection to {0} failed with code {1}".format(crumbURL, stat[1]))
        else:
            raise stat[1]
    httpresponse = stat[1]
    #Grab the cookie from the http header
    cookiestr = httpresponse.getheader('set-cookie')
    cookiestr = cookiestr.split('; expires')[0]
    cookie = cookiestr
    
    #Grab the crumb from the webpage
    webpageLines = []
    for bline in  httpresponse:
        #unicode-escape is used as there are times when the unicode character
        #\u004 exists within the string. Unicode-escape handles it fine.
        linestr = bline.decode('unicode-escape')
        webpageLines.append(linestr)
    crumb = None
    for line in webpageLines:
        index = line.find("Crumb")
        if not index == -1:
            endIndex = line.find("}", index)
            crumb = line[index : endIndex + 1]
    crumb = crumb.split(":")[-1][:-2]
    #First character of the crumb is a quotation mark, and is not a valid part of the crumb.
    return [cookie, crumb[1:]]

def buildURL (ticker, startDate, endDate, crumb):
    '''Builds URL for data retrieval
        @param ticker: ticker of the stock to retrieve data for
        @type ticker: String
        @param startDate: POSIX timestamp for the date to begin obtaining data for
        @type startDate: int
        @param endDate: POSIX timestamp for the final date to obtain data for
        @type endDate: int
        @param crumb: Crumb to use for data retrieval, obtained from getCrumbAndCookie
        @type crumb: String
        @return: URL used to obtain data from
        @rtype: String
    '''
    return baseURL.format(ticker, startDate, endDate, crumb)

def convertString(in_str, flag='float'):
    '''Converts the given string into its numeric representation with basic error correction
    @param in_str: String to be converted
    @type in_str: String
    @param flag: Flag to specify which conversion to attempt
    @type flag: String. Accepted values: 'float' or 'int'
    @return: Numeric representation of the string provided, -1 if a ValueError occurs, or None if a TypeError occurs
    @rtype: float or int, depending on the flag, or None if TypeError occurs
    '''
    if flag == 'float':
        try:
            ret = float(in_str)
        except ValueError:
            ret = -1
        except TypeError:
            ret = None
    elif flag == 'int':
        try:
            ret = int(in_str)
        except ValueError:
            ret = -1
        except TypeError:
            ret = None    
    
    return ret


def formatDayData(data):
    '''Formats the provided data string into storage format
    @param data: Data string to format
    @type data: string
    @return: Array of data extracted and formatted from string
    @rtype: [datetime.datetime, float, float, float, float, float, int]
    '''
    
    split = data.rstrip().split(",")
    day = dt.strptime(split[0], "%Y-%m-%d")
    open_price = convertString(split[1])
    high_price = convertString(split[2])
    low_price = convertString(split[3])
    close_price = convertString(split[4])
    adj_close = convertString(split[5])
    volume_data = convertString(split[6], flag='int')
    return [day, open_price, high_price, low_price, close_price, adj_close, volume_data]
    

def getDataFromURL(url, ticker, cookie):
    '''Obtains data from the URL
        @param url: URL to obtain data for
        @type url: String
        @param ticker: Ticker to assign to the data storage object
        @type ticker: String
        @param cookie: 
        
        Cookie to use for connection to Yahoo Servers
        Obtained from getCookieAndCrumb
        @type cookie: String
        @return: Data storage object containing the retrieved data
        @rtype: TickerDataStorage
    '''
    data = []
    status = openURL(url, cookie=cookie);
    if (status[0]):
        reply = status[1]
        for line in reply:
            data.append(line.decode());
        data = data[1:] #Removes the first line, which just says the format the data is in
    else:
        if (type(status[1]) == type(4)):
            raise ValueError("Ticker {0} errored with HTTP code {1}".format(ticker, status[1]));
        else:
            raise status[1];
    dataStorage = TickerDataStorage(ticker)
    for dayData in data:
        dataStorage.addData(formatDayData(dayData))
    return dataStorage;


