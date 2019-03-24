import sys
from datetime import datetime as dt

globalLogger = None

class GlobalLogger:
    
    '''Initializes a Logger with the specified output destination
    '''
    def __init__(self, outFile):
        self.outFile = outFile

    def __logTime(self):
        now = dt.now()
        print(now.strftime("%Y-%m-%d:%H:%M:%S"), file = self.outFile, end=': ')

    def logException(self, excep : Exception):
        '''Logs the exception given by excep with a timestamp
        '''
        self.__logTime()
        print(str(excep), file = self.outFile)

    def logWarning(self, warning : str):
        '''Logs the warning given by warning with a timestamp
        '''
        self.__logTime()
        print(warning, file = self.outFile)

def setupLogging(destinationFile):
    '''Sets up the global logger with the given destination'''
    global globalLogger
    globalLogger = GlobalLogger(destinationFile)

def getLogger():
    '''Returns an instance of the globally scoped logger'''
    return globalLogger