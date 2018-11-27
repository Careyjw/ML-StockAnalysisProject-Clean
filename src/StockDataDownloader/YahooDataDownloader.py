'''
Created on Nov 27, 2018

@author: Colton Freitas
@summary: 

Contains specialized methods to download stock data from Yahoo
'''

from .SharedUtilities import openURL

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
    return [cookie, crumb]

def buildURL (ticker, startDate, endDate, crumb):
    '''Builds URL for data retrieval
        @param ticker: ticker of the stock to retrieve data for
        @type ticker: String
        @param startDate: UNIX timestamp for the date to begin obtaining data for
        @type startDate: int
        @param endDate: UNIX timestamp for the final date to obtain data for
        @type endDate: int
        @param crumb: Crumb to use for data retrieval, obtained from getCrumbAndCookie
        @type crumb: String
        @return: URL used to obtain data from
        @rtype: String
    '''

