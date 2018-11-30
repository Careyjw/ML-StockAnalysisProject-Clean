'''
Created on Nov 27, 2018

@author: Colton Freitas
'''

from multiprocessing import pool
from time import sleep

class ModelTrainingPipeline:
    '''
    Class to handle using multiprocessing techniques to train models
    '''

    ''' Previous constructor header.
    def ___init__(self, max_processes, login_credentials, dataSelectionMethodID = 0, numClusteringProcesses = None, numTrainingProcesses = None) '''
    
    def __init__(self, max_processes, login_credentials, numClusteringProcesses = None, numTrainingProcesses = None):
        '''
        Constructor
        
        @param max_processes: Maximum number of processes to be created in the training process
        @param login_credentials: Login Credentials for the database accessing objects inside this class
        @param dataSelectionMethodID: ID of the data selection method. See setDataSelectionMethod
        @param numClusteringProcesses: Number of processes to be used for clustering, or None to automatically set value
        @param numTrainingProcesses: Number of processes to be used for training, or None to automatically set value
        '''
        
        self.trainingObjects = []
        self.numTrainingProcesses = numTrainingProcesses
        self.numClusteringProcesses = numClusteringProcesses
        #self.selectDataSelectionMethod(dataSelectionMethodID)
        self.loginCredentials = login_credentials
        self.maxProcesses = max_processes
        if (self.numClusteringProcesses == None):
            self.numClusteringProcesses = int(self.maxProcesses / 2)
        if (self.numTrainingProcesses == None):
            self.numTrainingProcesses = int(self.maxProcesses / 2)
        
    #===========================================================================
    # def selectDataSelectionMethod(self, sel_id):
    #     '''Sets the method to be used to process the data before training
    #     @param sel_id: The valid id's are defined in TrainingFunctionStorage.py and further information is given there
    #     '''
    #     pass
    # Removed for the time being. Until it is determined whether this is necessary.
    #===========================================================================
    
    def __clusterStocksIntoTrainingGroups(self, primaryTicker, loginCredentials, trainingPosition):
        '''Clusters stocks into training groups
        @param primaryTicker: Stock to compare all other stocks against
        @param loginCredentials: Login Credentials for the stock data retrieval
        @param trainingPosition: Value passed through to ensure that asyncronous creation of training processes
        do not overwrite. Return as the last element of the return array
        @return: [primaryTicker, [other tickers assigned based on similarity to primary], trainingPosition] or
        [trainingPosition] if ticker should not be trained
        
        This method is intended to be used by a multiprocess pool
        '''
        pass
    
    def __clusterCallback(self, resultsGiven):
        '''Adds returned tickers to a TrainingGroup object
        @param resultsGiven: Results returned from a clusteringFunction. Example given by return of __clusterStocksIntoTrainingGroups
        If return is just a one element array, training will not be done for the ticker
        
        '''
        trainingPosition = None
        if (len(resultsGiven) > 1):
            #ticker will be trained
            trainGroup = TrainingGroup(resultsGiven[0])
            for ticker in resultsGiven[1]:
                trainGroup.addTicker(ticker)
            args = (trainGroup, self.trainingFunctionArgs, self.loginCredentials)
            trainingPosition = resultsGiven[2]
            if (trainingPosition == 0):
                self.trainingAsyncWaitingList.append(self.trainingPool.apply_async(func = self.trainingFunction, args = args))
            else:
                isTurn = False
                while not (isTurn):
                    isTurn = True
                    for i in range(trainingPosition):
                        if (self.trainingAsyncWaitingListCheckIn[i]):
                            isTurn = False
                            break
                    sleep(1)
                self.trainingAsyncWaitingList.append(self.trainingPool.apply_async(func = self.trainingFunction, args = args))
        else:
            trainingPosition = resultsGiven[0]
        
        self.trainingAsyncWaitingListCheckIn[trainingPosition] = False
    
    def __addToAsyncWaitingList(self, waitingList, func, args, callback, pool, processCount):
        '''
        Handles adding an AsyncResult object to the waiting list without exceeding the processCount
        
        :param waitingList: List object to hold AsyncResult objects
        :param func: Function used in the pool.apply_async method
        :param args: args passed into func through pool.apply_async method
        :param callback: callback method passed into pool.apply_async method
        :param pool: Pool object used to achieve multiprocessing
        :param processCount: The maximum number of AsyncResult objects to have in the waiting list at once
        '''
        while True:
            print(waitingList)
            for i in range(len(waitingList)):
                if (waitingList[i].ready()):
                    del(waitingList[i])
                if(len(waitingList) < processCount):
                    waitingList.append(pool.apply_async(func = func, args = args, callback=callback))
                    return
            if(len(waitingList) < processCount):
                    waitingList.append(pool.apply_async(func = func, args = args, callback=callback))
                    return
            sleep(1)
        
    def __cleanAsyncList(self, waitingList):
        retList = []
        delList = []
        for i in range(len(waitingList)):
            if (waitingList[i].ready()):
                delList.append(waitingList[i])
        for i in range(len(delList)):
            retList.append(delList[i].get())
            waitingList.remove(delList[i])
        return retList
    
    def usePipeline(self, stockList, trainingFunction, trainingFunctionArgs, clusteringMethod = None):
        '''Handles clustering and use of training function for all tickers
        @param stockList: List of stock tickers to create models for
        @param trainingFunction: Function to be used for training models
        @type trainingFunction: Function
        @param trainingFunctionArgs: List type object for training function parameter passing
        This will be passed directly into the trainingFunction, so it is intended to be used
        For parameters that should be available and the same for all trainingFunction calls
        @param clusteringFunction: Either None or Function to be used for clustering stocks together
            If None, then default clustering method in this class is used
            
        :ClusteringFunctionArgumentList:
        Function header is identical to __clusterStocksIntoTrainingGroups
            
        :TrainingFunctionArugmentList: 
        <functionName>(trainingTickers : TrainingGroup, trainingFunctionArgs : list, loginCredentials : list)
        All training functions must have this function header, otherwise they will fail

        @return: List of return values from training functions
        '''
        
        
        numTickers = len(stockList)
        
        self.trainingFunction = trainingFunction
        self.trainingFunctionArgs = trainingFunctionArgs
        
        trainingPoolProcessCount = self.numTrainingProcesses
        clusteringPoolProcessCount = self.numClusteringProcesses
        
        self.clusteringPool = pool.Pool(clusteringPoolProcessCount)
        self.trainingPool = pool.Pool(trainingPoolProcessCount)
        
        self.trainingAsyncWaitingList = []
        self.trainingAsyncWaitingListCheckIn = [True] * numTickers
        
        clusteringAsyncWaitingList = []
        trainPos = 0
        for ticker in stockList:
            if not len(clusteringAsyncWaitingList) < clusteringPoolProcessCount:
                clusteringAsyncWaitingList.append(self.clusteringPool.apply_async(func = clusteringMethod, args = (ticker, self.loginCredentials, trainPos), callback = self.__clusterCallback))
            else:
                self.__addToAsyncWaitingList(clusteringAsyncWaitingList, clusteringMethod, (ticker, self.loginCredentials, trainPos), self.__clusterCallback, self.clusteringPool, self.numClusteringProcesses)
            trainPos += 1
        
        while not len(clusteringAsyncWaitingList) == 0:
            self.__cleanAsyncList(clusteringAsyncWaitingList)
            sleep(1)
        
        trainingRetList = []

        while not len(self.trainingAsyncWaitingList) == 0:
            trainingRetList.extend(self.__cleanAsyncList(self.trainingAsyncWaitingList))
            sleep(1)
        return trainingRetList
        
        
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
    
        
        
        
        
    