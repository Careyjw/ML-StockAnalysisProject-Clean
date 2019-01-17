from typing import List
from StockDataAnalysis.DataProcessingUtils import DataProcessor
from StockDataAnalysis.ClusteringUtils import calculateMovingAveragePercentageSimilarity
from datetime import datetime

def movingAverageClustering(ticker : str, loginCredentials : List[str], trainingPosition : int, clusterFunctionArguments : List):
    '''Calculates the most similar stocks for the stock given by ticker using the moving average
    :param ticker: Stock ticker to calculate similarities for
    :param loginCredentials: Credentials to access
    :param trainingPosition: Pass through value
    :clusterFunctionArgumentsFormat:
    [minimumSimilarity : float, maxNumberSimilarTickers : int, numDaysPerAverage : int, startDate : datetime] or

    :return: [primaryTicker, [other tickers assigned based on similarity to primary], trainingPosition] or
        [trainingPosition] if ticker should not be trained
    '''

    numDaysPerAverage = 14


    minimumSimilarity = clusterFunctionArguments[0]
    maxNumSimilarTickers = clusterFunctionArguments[1]
    numDaysPerAverage = clusterFunctionArguments[2]
    startDate = clusterFunctionArguments[3]

    dataMan = DataProcessor(loginCredentials)
    dataStorage = dataMan.getRawData(["hist_date", "adj_close"], startDate)
    mainTickerData = [x for x in dataStorage if x.ticker == ticker][0]
    otherTickerData = [x for x in dataStorage if not x.ticker == ticker]
    differenceScores = []
    for otherTicker in otherTickerData:
        simScore = calculateMovingAveragePercentageSimilarity(mainTickerData.data, otherTicker.data, numDaysPerAverage)
        if (simScore < 1):
            differenceScores.append( (simScore, otherTicker.ticker) )
    differenceScores = sorted(differenceScores, key= lambda var: var[0]) [:maxNumSimilarTickers]
    return [ticker, [x[1] for x in differenceScores if (1 - x[0]) >= minimumSimilarity], trainingPosition]



