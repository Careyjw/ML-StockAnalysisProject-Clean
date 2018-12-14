from configparser import ConfigParser, NoSectionError, NoOptionError

stockTickerFileLocation = "../configuration_data/stock_list.txt"
configurationFileLocation = "../configuration_data/config.ini"

def write_default_configs(parser, file_position):
    '''Creates the default configuration file in file_position with default values
    :param parser: ConfigParser object to write default configuration with
    :param file_position: String containing the path of the file to write the configuration to

    '''
    
    parser.add_section('login_credentials')
    parser.set('login_credentials', 'user', 'root')
    parser.set('login_credentials', 'password', "")
    parser.set('login_credentials', 'database', 'stock_testing')
    parser.set('login_credentials', 'host', 'localhost')
    fp = open(file_position, 'w')
    parser.write(fp)
    fp.close()

def config_handling():
    '''Does all of the configuration handling using the configparser package
    This uses a file location hard-built into this module, namely configurationFileLocation
    This function has the ability to write said file as well with default values
    @return: List of login credentials
    @rtype: [String, String, String, String]
    '''
    parser = ConfigParser()
    try:
        fp = open(configurationFileLocation, 'r')
        fp.close()
    except FileNotFoundError:
        write_default_configs(parser, configurationFileLocation)
    config_file = open(configurationFileLocation, 'r')
    parser.read_file(config_file)
    config_file.close()
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
    '''Obtains a list of all stock tickers to attempt to download
    
    '''
    file = open(stockTickerFileLocation, 'r')
    return_data = []
    for line in file:
        return_data.extend([line.strip()])
    file.close()
    return return_data