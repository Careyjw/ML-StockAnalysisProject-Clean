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
    
    def __init__(self, max_processes, login_credentials):
        '''
        Constructor
        
        @param max_processes: Maximum number of processes to be created in the training process
        @param login_credentials: Login Credentials for the database accessing objects inside this class
        '''
        
        self.trainingObjects = []
        self.loginCredentials = login_credentials
        self.maxProcesses = max_processes

    def __addToAsyncWaitingList(self, waitingList, func, args, pool, processCount):
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
            for i in range(len(waitingList)):
                if (waitingList[i].ready()):
                    del(waitingList[i])
                if(len(waitingList) < processCount):
                    waitingList.append(pool.apply_async(func = func, args = args))
                    return
            if(len(waitingList) < processCount):
                    waitingList.append(pool.apply_async(func = func, args = args))
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
            
    def usePipeline(self, stockList, trainingFunction, modelConfiguration):
        '''Handles clustering and use of training function for all tickers
        @param stockList: List of stock tickers to create models for
        @param trainingFunction: Function to be used for training models
        @type trainingFunction: Function
        @param trainingFunctionArgs: List type object for training function parameter passing
        This will be passed directly into the trainingFunction, so it is intended to be used
        For parameters that should be available and the same for all trainingFunction calls
        '''

        numTickers = len(stockList)
        
        self.trainingFunction = trainingFunction
        
        self.trainingPool = pool.Pool(self.maxProcesses)
        
        trainingAsyncWaitingList = []
        
        for ticker in stockList:
            trainingArgs = (ticker, modelConfiguration)
            self.__addToAsyncWaitingList(trainingAsyncWaitingList, trainingFunction, trainingArgs, self.trainingPool, self.maxProcesses)
        
        while not len(trainingAsyncWaitingList) == 0:
            self.__cleanAsyncList(trainingAsyncWaitingList)
            sleep(1)