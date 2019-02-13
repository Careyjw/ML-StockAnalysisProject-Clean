class ClusteredStockStorage:
    '''Storage class for training groups
    '''
    
    def __init__(self, primaryTicker):
        '''
        @param primaryTicker: The main ticker. 
        All other tickers in this class will be used to train a model to predict the primary ticker
        '''
        self.primaryTicker = primaryTicker
        self.trainingTickers = []
    
    def addTicker(self, ticker):
        '''Adds a ticker to the trainingTickers list'''
        self.trainingTickers.append(ticker)

    def getTrainingTickers(self):
        self.trainingTickers.append(self.primaryTicker)
        return self.trainingTickers