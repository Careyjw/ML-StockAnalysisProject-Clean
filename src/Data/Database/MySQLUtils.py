'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

import mysql.connector as connector
from mysql.connector.errors import Error as SQLError, InterfaceError
from datetime import date


updateStockListTableSQL = "update stock_list set {0}"
updateStockListTableSQLForTicker = updateStockListTableSQL + " where ticker = '{1}'"

database = "stock_testing"

stockListTableColList = ["ticker", "yahoo", "google"]
stockListTableCreationColList = [["id int primary key auto_increment"], [stockListTableColList[0], "text"], [stockListTableColList[1], "bool"], [stockListTableColList[2], "bool"] ]

tickerDataTableColList = ["hist_date", "opening_price", "high_price", "low_price", "close_price", "adj_close", "volume_data"]
tickerDataTableCreationColList = [["id int primary key auto_increment"], [tickerDataTableColList[0], "Date"], [tickerDataTableColList[1], "float"],
                     [tickerDataTableColList[2], "float"], [tickerDataTableColList[3], "float"], [tickerDataTableColList[4], "float"], [tickerDataTableColList[5], "float"],
                     [tickerDataTableColList[6], "long"]]

tableNameBaseString = "{0}_{1}_data"
#Example formatting of above: tableNameBaseString.format(ticker, sourceName)

def connect(host, user, password, database = None):
    '''Creates and returns a MYSQL database connection
    @param host: Host to connect to
    @type host: String
    @param user: User to connect to
    @type user: String
    @param password: The password to connect with
    @type password: String
    @param database: Optional, database to connect to
    @type database: String or None
    @return: List specified in rformat
    @rformat: [True, SQLConnection] or [False, SQLError]
    '''
    ret = None
    try:
        if database == None:
            ret = connector.connect(host = host, user = user, password = password)
        else:
            ret = connector.connect(host = host, user = user, password = password, database = database)
    except SQLError as e:
        ret = [False, e]
    return [True, ret]


class MYSQLDataManipulator:
    '''Convenience class to handle interfacing with the MySQL database
    
    #TODO: Change error handling in class to be more customized and informative
    '''


    def __init__(self, host, user, password, database=None):
        '''Initializes object and performs connection
        @param host: Host to connect to
        @type host: String
        @param user: User to connect to
        @type user: String
        @param password: The password to connect with
        @type password: String
        @param database: Optional, database to connect to
        @type database: String or None
        '''
        connectionStatus = connect(host, user, password, database)
        if (connectionStatus[0]):
            self.connection = connectionStatus[1]
        else:
            raise connectionStatus[1]
        if (type(self.connection) == type([])):
            raise ConnectionError(self.connection[1])
        self.currentDatabase = database
        self.cursor = None
        
    def insert_into_table(self, table, column_names, data, database = None):
        ''' Uploads the information in data into the table specified
        
        @param column_names: List containing the names of the slots to put each column of data into
        @type column_names: [String, String ...., String]
        @param data: List of data to insert into the table, len(data) must equal len(column_names),
            :NOTE: data is assumed to be a 2D array of data sets to insert, so to insert one element
            It must be passed as [[element]]
        @type data: specified by column_names
        @param database: The database the table is stored in, if this is None, then the database currently
            focused by the connection is used. The database used is kept between calls to this method.
        @type database: String or None

        '''
        
        self.cursor = self.connection.cursor()
        if not database == None:
            self.switch_database(database)
        else:
            self.switch_database(self.currentDatabase)
        
        col_string = ",".join(column_names)
        
        insertion_sql = "INSERT INTO %s (%s) VALUES" % (table, col_string)
        insertion_sql += '(' + (','.join(['%s'] * len(column_names))) + ')'
        for to_insert in data:
            self.cursor.execute(insertion_sql, to_insert)
        
    def __close_cursor(self, cursor):
        '''Closes specified cursor
        '''
        if not cursor.close():
            self.connection.close()
            raise ConnectionError("Cursor refused to close, cleaning up and exiting")
        
    def checkDatabaseExistence(self, database, create=False):
        '''Checks if the database provided by database exists, optionally creating it
        @param database: The database to check for existence
        @type database: String
        @param create: Flag designating whether to create the database if it does not exist
        @type create: boolean
        @return: True if the database exists, or is created, False if the database does not exist or cannot be created
        @rtype: boolean
        '''

        conditionalString = 'where SCHEMA_NAME = "{0}"'.format(database)

        res = self.select_from_table("schemata", ["SCHEMA_NAME"], conditional=conditionalString, database="INFORMATION_SCHEMA")
        if(len(res) == 0):
            if (create):
                self.create_database(database)
                return True
            return False
        return True

    def checkTableExistence(self, tableName, create=False, columnDeclarationList = None):
        '''Checks if the table provided by tableName exists in the current database, optionally creating it if not 
        :param tableName: Name of the table to check for
        :param create: Flag toggling creation of the table if it does not exist
        :param columnDeclarationList: If create is True, then this is the column declaration list to use for creating the table
        '''
        prevDatabase = self.currentDatabase
        conditionalString = 'where TABLE_SCHEMA = "{0}" and TABLE_NAME = "{1}"'.format(prevDatabase, tableName)
        res = self.select_from_table("tables", ["TABLE_NAME"], conditional=conditionalString, database="INFORMATION_SCHEMA")
        self.switch_database(prevDatabase)
        if (len(res) == 0):
            if (create and not columnDeclarationList == None):
                self.create_table(tableName, columnDeclarationList, prevDatabase)
                return True
            return False
        return True
        
    def create_database(self, database):
        '''Creates the specified database
        @param database: The database to create
        @type database: String
        @return: True if database was created, False otherwise
        '''
        if not (self.checkDatabaseExistence(database)):
            self.cursor = self.connection.cursor()
            self.execute_sql("create schema " + database)
            return True
        return False
        
    def create_table(self, table_name, columns, database = None):
        ''' Creates a table in the database specified 
        
        @param columns: List of lists containing strings of the slot's name, followed by its type, and then any extra parameters needed
            for the slot creation. (I.E. 'primary key', 'auto_increment', etc)
        @param database: The database to create a new table in, if value is None, then uses the currently used database
        '''
        
        #assuming parameter columns is in the form of [ ['id', 'int', 'primary key', 'auto_increment'], ['col1', 'text'] ... ]
        
        self.cursor = self.connection.cursor()
        
        if not database == None:
            self.switch_database(database)
        else:
            self.switch_database(self.currentDatabase)
        
        column_declarations = []
        
        for column_declaration in columns:
            column_declarations.extend([" ".join(column_declaration)])
        
        columnString = ",".join(column_declarations)
        
        table_creation_sql = "create table %s (%s)" % (table_name, columnString)
        
        
        self.cursor.execute(table_creation_sql)
        
    def switch_database(self, database):
        ''' Switches the database the DataManipulator is using 
        @param database: The name of the database to use
        @type database: String
        @param cursor: A cursor instance created from the current connection.
        @type cursor: Cursor
        '''
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE %s" % database)
        self.currentDatabase = database
        
    def select_from_table(self, table_name, column_list, database = None, conditional = None):
        '''Performs the specified SELECT command on the given table
        @param table_name: Name of the table to SELECT from
        @type table_name: String
        @param column_list: List of columns to retrieve data from
        @type column_list: [String...]
        @param database: Optional, Database to retrieve data from. None will use current database
        @type database: String
        @param conditional: Optional, full conditional string to add to the SELECT command. If none, no conditional is added
        @type conditional: String
        @format conditional: "if|where <conditional>"
        @return iterator over the returned data
        '''
        column_string = ",".join(column_list)
        
        sql = "select %s from %s" % (column_string, table_name)
        
        if not conditional == None:
            sql += " %s" % conditional
        
        self.cursor = self.connection.cursor()
        
        if not database == None:
            self.switch_database(database)
        else:
            self.switch_database(self.currentDatabase)
        self.cursor.execute(sql)
        ret_iter = self.cursor.fetchall()
        
        return ret_iter

    def execute_sql(self, sql):
        '''Method to execute a piece of SQL code directly, more for niche usage than normal use
        @param sql: Full sql code to execute
        @type sql: String
        @return: Iterator over any data that may have been returned
        '''
        self.cursor = self.connection.cursor()
        self.switch_database(self.currentDatabase)
        
        self.cursor.execute(sql)
        ret_iter = None
        try:
            ret_iter = self.cursor.fetchall()
        except InterfaceError:
            pass
        
        return ret_iter
    
    def commit(self):
        '''
        connection.commit() wrapper
        '''
        self.connection.commit()
    
    def rollback(self):
        '''
        connection.rollback() wrapper
        '''
        self.connection.rollback()
        
    def close(self, commit=True):
        '''Convenience close method
        @param commit: Boolean specifying whether to commit before closing or not
        '''
        if commit:
            self.connection.commit()
        self.connection.close()
        
def clearDataFromStockListTable(dataManipulator):
    '''Sets the value of all columns except for ticker and id in stock_list to False
    @param dataManipulator: The MYSQLDataManipulator object to use to upload
    @type dataManipulator: MYSQLDataManipulator
    '''
    
    sources = [x+"=0" for x in stockListTableColList[1:]]
    sourcesString = ", ".join(sources)
    sql = updateStockListTableSQL.format(sourcesString) + ";"
    dataManipulator.execute_sql(sql)
    dataManipulator.commit()

def updateStockListTableAfterDataInsertion(dataManipulator, ticker, source):
    '''
    @param dataManipulator: The MYSQLDataManipulator object to use to upload
    @type dataManipulator: MYSQLDataManipulator
    @param ticker: String of the stock ticker
    @param source: Name of source to update for
    '''

    sql = updateStockListTableSQLForTicker + ";"
    sql = sql.format(source+"=1", ticker)
    dataManipulator.execute_sql(sql)
    dataManipulator.commit()

        
def uploadData(sourceData, dataManipulator):
    '''Uploads the provided SourceDataStorage object's data to the MySQL database
    @param sourceData: The data storage object to upload data from
    @type sourceData: SourceDataStorage
    @param dataManipulator: The MYSQLDataManipulator object to use to upload
    @type dataManipulator: MYSQLDataManipulator
    '''
    
    storedTickers = dataManipulator.select_from_table("stock_list", ["ticker"], database=database)
    storedTickers = [x[0] for x in storedTickers]

    for tickerStorage in sourceData.tickers:
        tableName = tableNameBaseString.format(tickerStorage.ticker, sourceData.sourceName)
        tickerInStorage = tickerStorage.ticker in storedTickers
        if (tickerStorage.ticker in storedTickers) and (dataManipulator.checkTableExistence(tableName)):
            #Collect all dates and do comparison to populate database
            stored_days = dataManipulator.select_from_table(tableName, ["hist_date"])
            stored_days = [x[0] for x in stored_days]
            for dataSet in tickerStorage.data:
                currentDataDay = date.fromtimestamp(dataSet[0].timestamp())
                if not (currentDataDay in stored_days):
                    dataManipulator.insert_into_table(tableName, tickerDataTableColList, [dataSet])
        else: 
            dataManipulator.checkTableExistence(tableName, create=True, columnDeclarationList = tickerDataTableCreationColList)
            for dataSet in tickerStorage.data:
                dataManipulator.insert_into_table(tableName, tickerDataTableColList, [dataSet])
            if not (tickerInStorage):
                #If ticker was not stored in stock_list, then it needs to be added
                dataManipulator.insert_into_table("stock_list", stockListTableColList, [[tickerStorage.ticker, 0, 0]])
                #Otherwise, it just needs its source updated after table creation
        updateStockListTableAfterDataInsertion(dataManipulator, tickerStorage.ticker, sourceData.sourceName)
    dataManipulator.commit()



def createStockDatabase(dataManipulator):
    '''Creates the standard stock database format, defined below
    :param dataManipulator: MYSQLDataManipulator object used to create the database
    :format:

    Database is listed under the schema "stock_testing",
    Inside it initially will just be a single table, stock_list,
    Which will hold the following rows:
        ticker (will be a valid stock ticker {i.e. 'AAPL'})
        another column for each data source (currently two),
            which will store a boolean
    '''
    
    dataManipulator.checkDatabaseExistence(database, create=True)
    dataManipulator.switch_database(database)
    dataManipulator.checkTableExistence("stock_list", create=True, columnDeclarationList=stockListTableCreationColList)


