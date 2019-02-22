from typing import List

def combineDataSets(dataSets : List[List[List]]):
    '''Combines data sets together
    dataSets format:
        List of dataSets containing data in the following format:
            [hist_date, data]
    Removes dates and combines the data in the following way
    retData = [[data0[0], data1[0] ... dataN[0]] ... ]
    '''
    nonDatedData = []
    for dataSet in dataSets:
        nonDatedData.append( [x[1] for x in dataSet] )

    retData = []
    for i in range(len(nonDatedData[0])):
        retData.append([])

    for i in range(len(retData)):
        for dataSet in nonDatedData:
            retData[i].append(dataSet[i])

    return retData

def genTargetExampleSets(targetDataSet : List, examplesPerSet : int):
    '''Generate a list of target data example sets
    Each set will contain examplesPerSet number of data from the data set
    Each set overlaps examplesPerSet-1 number of data values
    '''
    retlist = []
    numExamplesGenerated = len(targetDataSet) - examplesPerSet
    for i in range(numExamplesGenerated):
        shiftedIndex = i+1
        retlist.append( targetDataSet[ shiftedIndex:shiftedIndex + examplesPerSet ] )
    return retlist

def genTrainingExampleSets(trainDataSet : List[List], examplesPerSet : int):
    '''Generate a list of training data example sets
    Each set will contain examplesPerSet number of data from the data set
    Each set overlaps examplesPerSet-1 number of data values
    '''
    retlist = []
    numExamplesGenerated = len(trainDataSet) - examplesPerSet
    for i in range(numExamplesGenerated):
        retlist.append( trainDataSet[ i:i+examplesPerSet] )

    return retlist