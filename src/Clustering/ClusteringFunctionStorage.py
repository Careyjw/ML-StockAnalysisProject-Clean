from typing import List
from Data.ModelDataProcessing.DataProcessingUtils import DataProcessor
from Clustering.ClusteringUtils import calculateMovingAveragePercentageSimilarity
from datetime import datetime

def movingAverageClustering(modelConfiguration):
    '''Calculates the most similar stocks for the stock given by ticker using the moving average
    :param ticker: Stock ticker to calculate similarities for
    :param loginCredentials: Credentials to access
    :param trainingPosition: Pass through value
    :clusterFunctionArgumentsFormat:
    [minimumSimilarity : float, maxNumberSimilarTickers : int, numDaysPerAverage : int, startDate : datetime] or

    :return: [primaryTicker, [other tickers assigned based on similarity to primary]]
    '''
    ticker = modelConfiguration['General']['sTicker']
    startDate = modelConfiguration['General']['dtStartingDate']
    endDate = modelConfiguration['General']['dtEndingDate']
    loginCredentials = modelConfiguration['General']['lsLoginCredentials']
    
    minimumSimilarity = float(modelConfiguration['General']['fMinimumSimilarity'])
    maxNumSimilarTickers = int(modelConfiguration['General']['iMaxTrainingTickers'])
    numDaysPerAverage = int(modelConfiguration['General']['iNumberDaysPerExample'])

    dataMan = DataProcessor(loginCredentials)
    dataStorage = dataMan.getRawData(["hist_date", "adj_close"], startDate, endDate)
    mainTickerData = [x for x in dataStorage if x.ticker == ticker][0]
    otherTickerData = [x for x in dataStorage if not x.ticker == ticker]
    differenceScores = []
    for otherTicker in otherTickerData:
        simScore = calculateMovingAveragePercentageSimilarity(mainTickerData.data, otherTicker.data, numDaysPerAverage)
        if (simScore < 1):
            differenceScores.append( (simScore, otherTicker.ticker) )
    differenceScores = sorted(differenceScores, key= lambda var: var[0]) [:maxNumSimilarTickers]
    return [x[1] for x in differenceScores if (1 - x[0]) >= minimumSimilarity]



