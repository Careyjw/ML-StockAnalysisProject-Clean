from datetime import datetime
from typing import List
from StockDataAnalysis.DataProcessingUtils import calculatePercentageChange
from StockDataAnalysis.VolumeDataProcessing import calcSign

def calculateMovingAverageForPeriod(period : List[float], numDaysPerAverage : int) -> List[float]:
    '''Calculates the moving average for the supplied period's data
    :param period: List of data to calculate the moving average for
    :param numDaysPerAverage: Number of days to use to calculate the moving average
    '''
    movingAverageStorage = []
    for i in range(numDaysPerAverage-1):
        movingAverageStorage.append(average(period[:i+1]))
    for i in range(len(period) - (numDaysPerAverage-1)):
        movingAverageStorage.append(average(period[i:numDaysPerAverage+i]))
    return calculatePercentageChangesForPeriod(movingAverageStorage)

def average(vals : List[float]):
    '''Calculates the average value contained within the list
    '''
    avg = 0
    for x in vals:
        avg += x
    return avg / len(vals)

def calculatePercentChangeTwoMovingAverages(average1, average2):
    '''Calculates the percentage change between two moving average numbers
    This algorithm is equivalent to comparing the movement directions of the two 
    passed parameters
    '''
    signAverage1 = calcSign(average1)
    signAverage2 = calcSign(average2)
    if (signAverage1 == signAverage2):
        return 0
    elif (signAverage1 == -1):
        return 100
    else:
        return -100

def calculatePercentageChangesForPeriod(period : List[float]) -> List[float]:
    '''Calculates the percentage changes for the period data given
    '''
    retList = []
    for i in range(len(period) - 1):
        retList.append(calculatePercentageChange (period[i], period[i+1]) )
        
    return retList

def calculateMovingAveragePercentageSimilarity(ticker1Data : List[ List["datetime, float"] ], ticker2Data : List[ List["datetime, float"] ], numDaysPerAverage : int) -> float:
    '''Calculates the percentage similarity between the moving averages using the data supplied in ticker1Data and ticker2Data
    '''
    ticker1StartDate = ticker1Data[0][0]
    ticker2StartDate = ticker2Data[0][0]
    #if ticker1 and ticker2's start date are not the same,
    #They will have different amounts of data...
    #And therefore cannot be used with each other
    if not ticker1StartDate == ticker2StartDate or not len(ticker1Data) == len(ticker2Data):
        return 100

    ticker1MovingAverage = calculateMovingAverageForPeriod( [x[1] for x in ticker1Data], numDaysPerAverage )
    ticker2MovingAverage = calculateMovingAverageForPeriod( [x[1] for x in ticker2Data], numDaysPerAverage )
    movingAveragePercentageChanges = [calculatePercentChangeTwoMovingAverages(ticker1MovingAverage[i], ticker2MovingAverage[i]) for i in range(len(ticker1MovingAverage))]
    absoluteDifference = 0
    for x in movingAveragePercentageChanges:
        absoluteDifference += abs(x)
    return (absoluteDifference / len(ticker1MovingAverage)) / 100