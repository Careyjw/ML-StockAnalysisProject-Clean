'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from Common.Util.CommonFunctions import config_handling, get_stock_list
from StockDataDownloader.DataDownloadSources import DownloadDataYahoo
from DatabaseUtils.MySQLUtils import uploadData, MYSQLDataManipulator, createStockDatabase, clearDataFromStockListTable


if __name__ == '__main__':
    login_credentials = config_handling()
    stock_list = get_stock_list()
    YahooData = DownloadDataYahoo(stock_list)
    data_manager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2])
    createStockDatabase(data_manager)
    clearDataFromStockListTable(data_manager)
    uploadData(YahooData, data_manager)
    data_manager.close(commit = True)
    print("Fin.")
    
    
    
    



