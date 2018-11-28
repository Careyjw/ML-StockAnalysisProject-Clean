'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

class ModelTrainingPipeline:
    '''
    Class to handle using multiprocessing techniques to train models
    '''


    def __init__(self, max_processes, login_credentials, maxTrainingTickers, dataSelectionMethodID = 0, numClusteringProcesses = None, numTrainingProcesses = None):
        '''
        Constructor
        
        @param max_processes: Maximum number of processes to be created in the training process
        @param login_credentials: Login Credentials for the database accessing object inside this class
        @param maxTrainingTickers: Maximum number of other stocks used to train each stock
        @param dataSelectionMethodID: ID of the data selection method. See setDataSelectionMethod
        @param numClusteringProcesses: Number of processes to be used for clustering, or None to automatically set value
        @param numTrainingProcesses: Number of processes to be used for training, or None to automatically set value
        '''
        
        self.trainingObjects = []
        
        pass
        
    def selectDataSelectionMethod(self, sel_id):
        '''Sets the method to be used to process the data before training
        @param sel_id: The valid id's are defined in TrainingFunctionStorage.py and further information is given there
        '''
        pass
    
    def __clusterStocksIntoTrainingGroups(self, primaryTicker, loginCredentials):
        '''Clusters stocks into training groups
        @param primaryTicker: Stock to compare all other stocks against
        @param loginCredentials: Login Credentials for the stock data retrieval
        @return: [primaryTicker, [other tickers assigned based on similarity to primary]
        
        This method is intended to be used by a multiprocess pool
        '''
        pass
    
    def __clusterCallback(self, resultsGiven):
        '''Adds returned tickers to a TrainingGroup object
        @param resultsGiven: Results returned from __clusterStocksIntoTrainingGroups
        If None, no training is done for this ticker
        
        '''
        pass
    
    def usePipeline(self, trainingFunction, trainingFunctionArgs, clusteringMethod = None):
        '''Handles clustering and use of training function for all tickers
        @param trainingFunction: Function to be used for training models
        @type trainingFunction: Function
        @param trainingFunctionArgs: List type object for training function parameter passing
        @param clusteringFunction: Either None or Function to be used for clustering stocks together
            If None, then default clustering method in this class is used
        
        '''
        pass
        
        
class TrainingGroup:
    '''Storage class for training groups
    '''
    
    def __init__(self, primaryTicker):
        '''
        @param primaryTicker: The main ticker. 
        All other tickers in this class will be used to train a model to predict the primary ticker
        '''
        self.primaryTicker = primaryTicker;
        self.trainingTickers = []
        pass
    
    def addTicker(self, ticker):
        '''Adds a ticker to the trainingTickers list'''
        self.trainingTickers.append(ticker)
    
        
        
        
        
    