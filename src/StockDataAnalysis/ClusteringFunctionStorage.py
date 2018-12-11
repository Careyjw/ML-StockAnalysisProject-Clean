from typing import List
from StockDataAnalysis.DataProcessingUtils import DataProcessor
from StockDataAnalysis.ClusteringUtils import calculateMovingAveragePercentageSimilarity
from datetime import datetime

startDate : datetime = None
clusterFunctionArguments = None

def setClusterFunctionArgs(clusterFunctionArgs : List):
    '''Sets cluster function args for all clustering methods
    '''
    global clusterFunctionArguments
    clusterFunctionArguments = clusterFunctionArgs

def setStartDate(startingDate : datetime):
    '''Sets starting date for all clustering methods
    '''
    global startDate
    startDate = startingDate

def movingAverageClustering(ticker : str, loginCredentials : List[str], trainingPosition : int):
    '''Calculates the most similar stocks for the stock given by ticker using the moving average
    :param ticker: Stock ticker to calculate similarities for
    :param loginCredentials: Credentials to access
    :param trainingPosition: Pass through value
    :clusterFunctionArgumentsFormat:
    [minimumSimilarity : float, maxNumberSimilarTickers : int, numDaysPerAverage : int] or
    [minimumSimilarity : float, maxNumberSimilarTickers : int]

    :return: [primaryTicker, [other tickers assigned based on similarity to primary], trainingPosition] or
        [trainingPosition] if ticker should not be trained
    '''
    global startDate
    global clusterFunctionArguments

    numDaysPerAverage = 14

    if len(clusterFunctionArguments) == 3:
        numDaysPerAverage = clusterFunctionArguments[2]

    minimumSimilarity = clusterFunctionArguments[0]
    maxNumSimilarTickers = clusterFunctionArguments[1]

    dataMan = DataProcessor(loginCredentials)
    dataStorage = dataMan.getRawData(["hist_date", "adj_close"], startDate)
    mainTickerData = [x for x in dataStorage if x.ticker == ticker][0]
    otherTickerData = [x for x in dataStorage if not x.ticker == ticker]
    differenceScores = []
    for otherTicker in otherTickerData:
        simScore = calculateMovingAveragePercentageSimilarity(mainTickerData.data, otherTicker.data, numDaysPerAverage)
        print(simScore, otherTicker.ticker)
        if (simScore < 1):
            differenceScores.append( (simScore, otherTicker.ticker) )
    differenceScores = sorted(differenceScores, key= lambda var: var[0]) [:maxNumSimilarTickers]
    return [ticker, [x[1] for x in differenceScores if (1 - x[0]) >= minimumSimilarity], trainingPosition]



