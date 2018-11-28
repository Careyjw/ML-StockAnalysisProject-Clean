'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from configparser import ConfigParser, NoSectionError, NoOptionError
from StockDataDownloader.DataDownloadSources import DownloadDataYahoo
from DatabaseUtils.MySQLUtils import uploadData, MYSQLDataManipulator
from EmailUtils.SimpleEmailSender import SimpleEmailSender


stockTickerFileLocation = "../configuration_data/stock_list.txt"
configurationFileLocation = "../configuration_data/config.ini"


def write_default_configs(parser, file_position):
    '''Creates the default configuration file in file_position with default values'''
    
    parser.add_section('login_credentials')
    parser.set('login_credentials', 'user', 'root')
    parser.set('login_credentials', 'password', "")
    parser.set('login_credentials', 'database', 'stock_testing')
    parser.set('login_credentials', 'host', 'localhost')
    fp = open(file_position, 'w')
    parser.write(fp)
    fp.close()

def config_handling():
    '''does all of the configuration handling using the configparser package'''
    parser = ConfigParser()
    try:
        fp = open(configurationFileLocation, 'r')
        fp.close()
    except FileNotFoundError:
        write_default_configs(parser, configurationFileLocation)
    config_file = open(configurationFileLocation, 'r')
    parser.read_file(config_file)
    try:
        user = parser.get('login_credentials', 'user')
        password = parser.get('login_credentials', 'password')
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    except (NoSectionError, NoOptionError):
        write_default_configs(parser, configurationFileLocation)
        user = parser.get('login_credentials', 'user')
        password = parser.get('login_credentials', 'password')
        database = parser.get('login_credentials', 'database')
        host = parser.get('login_credentials', 'host')
    return [host, user, password, database]

def get_stock_list():
    '''Obtains a list of all stock tickers to attempt to download'''
    file = open(stockTickerFileLocation, 'r')
    return_data = []
    for line in file:
        return_data.extend([line.strip()])
    file.close()
    return return_data




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
    
    
    
    
    



