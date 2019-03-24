'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from Common.Util.CommonFunctions import config_handling, get_stock_list, loginCredentialAssembling
from Download.DataDownloadSources import DownloadDataYahoo
from Download.GlobalDownloadLogger import setupLogging, getLogger
from Data.Database.MySQLUtils import uploadData, MYSQLDataManipulator, createStockDatabase, clearDataFromStockListTable
from sys import stderr
from argparse import ArgumentParser
from getpass import getpass

def parseArgs():
    parser = ArgumentParser(description="Data Download script")
    parser.add_argument("-dp", dest='dp', help="Password for database access, can be passed in or typed at prompt that will appear", default=None)
    parser.add_argument("-f", dest='f', help="Path to a file for a log to be created at, otherwise, defaults to system ouput", default = None)
    namespace = parser.parse_args()
    if namespace.dp == None:
        namespace.dp = getpass('Database Password:')
    return namespace

def setupGlobalLogger(fileName):
    destFile = stderr
    shouldClose = False
    if not fileName == None:
        destFile = open(namespace.f, 'w')
        shouldClose = True
    setupLogging(destFile)
    return [shouldClose, destFile]

if __name__ == '__main__':
    namespace = parseArgs()
    shouldClose, destFile = setupGlobalLogger(namespace.f)
    login_credentials = loginCredentialAssembling(namespace.dp)
    stock_list = get_stock_list()
    YahooData = DownloadDataYahoo(stock_list)
    data_manager = None
    try:
        data_manager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2])
    except Exception as e:
        logger = getLogger()
        logger.logException(e)
        logger.logWarning("Exception is irrecoverable, exiting...")
        exit(2)
    createStockDatabase(data_manager)
    clearDataFromStockListTable(data_manager)
    uploadData(YahooData, data_manager)
    data_manager.close(commit = True)
    print("Fin.")
    if shouldClose:
        destFile.close()
    
    
    
    



