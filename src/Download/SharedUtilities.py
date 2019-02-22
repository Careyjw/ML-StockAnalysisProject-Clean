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
    