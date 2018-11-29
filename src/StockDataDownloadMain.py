'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from SharedGeneralUtils.SharedGeneralUtils import config_handling, get_stock_list
from StockDataDownloader.DataDownloadSources import DownloadDataYahoo
from DatabaseUtils.MySQLUtils import uploadData, MYSQLDataManipulator
from EmailUtils.SimpleEmailSender import SimpleEmailSender


if __name__ == '__main__':
    login_credentials = config_handling()
    stock_list = get_stock_list()
    YahooData = DownloadDataYahoo(stock_list)
    data_manager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2], login_credentials[3])
    uploadData(YahooData, data_manager)
    data_manager.close(commit = True)
    smtpServer = SimpleEmailSender(host="smtp.gmail.com", port=465, username="mlstockpredictions@gmail.com", password="PrayersAndFaith")
    smtpServer.sendMessage("Hello,\n\tThis message is to inform you that the program, DailyStockDataDownloader, has successfully completed its task. Have a nice day!", "Program Result", to = "freitacr@plu.edu", user_from="Machine Learning Stock Predictions")
    smtpServer.close();
    print("Fin.")
    
    
    
    
    



