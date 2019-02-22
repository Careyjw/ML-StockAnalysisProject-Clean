'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from Common.Util.CommonFunctions import config_handling, get_stock_list, loginCredentialAssembling
from Download.DataDownloadSources import DownloadDataYahoo
from Data.Database.MySQLUtils import uploadData, MYSQLDataManipulator, createStockDatabase, clearDataFromStockListTable
from argparse import ArgumentParser
from getpass import getpass

def parseArgs():
    parser = ArgumentParser(description="Data Download script")
    parser.add_argument("-dp", dest='dp', help="Password for database access, can be passed in or typed at prompt that will appear", default=getpass('Database Password:'))
    return parser.parse_args()


if __name__ == '__main__':
    namespace = parseArgs()
    login_credentials = loginCredentialAssembling(namespace.dp)
    stock_list = get_stock_list()
    YahooData = DownloadDataYahoo(stock_list)
    data_manager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2])
    createStockDatabase(data_manager)
    clearDataFromStockListTable(data_manager)
    uploadData(YahooData, data_manager)
    data_manager.close(commit = True)
    print("Fin.")
    
    
    
    



