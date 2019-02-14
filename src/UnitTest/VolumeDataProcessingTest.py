import unittest
from Common.Util.CommonFunctions import config_handling
from DatabaseUtils.MySQLUtils import MYSQLDataManipulator, stockListTableColList, stockListTableCreationColList, tickerDataTableColList, tickerDataTableCreationColList
from StockDataAnalysis.VolumeDataProcessing import VolumeDataProcessor
from datetime import datetime as dt, timedelta as td

expectedSignedPercentageChangeResultsReal = [ 11.29594998, -190.6811398, -5.359109409, -202.8384959 ]
expectedUnsignedPercentageChangeResultsReal = [ 11.29594998, -9.318860244, -5.359109409, 2.838495883 ]

expectedSignedPercentageChangeResultsPos = [ 100, 50, 33.3333333, 25 ]
expectedUnsignedPercentageChangeResultsPos = [ 100, 50, 33.3333333, 25 ]

expectedSignedLNCResultsReal = [11, -191, -5, -203]
expectedUnsignedLNCResultsReal = [11, -9, -5, 3]

expectedSignedLNCResultsPos = [100, 50, 33, 25]
expectedUnsignedLNCResultsPos = [100, 50, 33, 25]

expectedSignedMovementDirectionResultsReal = ['up', 'down', 'down', 'down']
expectedUnsignedMovementDirectionResultsReal = ['up', 'down', 'down', 'up']

expectedSignedMovementDirectionResultsPos = ['up', 'up', 'up', 'up']
expectedUnsignedMovementDirectionResultsPos = ['up', 'up', 'up', 'up']

def genPosData():
    '''Populates a data array with a completely fake dataset, designed to be increasing incrementally only.
    '''
    data = []
    baseDataSet = [dt.now() - td(18), 1, 2, 0, 1, 1, 300]
    for i in range(5):
        data.append([
            baseDataSet[0] + (td(1) * i),
            baseDataSet[1] + i,
            baseDataSet[2] + i,
            baseDataSet[3] + i,
            baseDataSet[4] + i,
            baseDataSet[5] + i,
            baseDataSet[6] + (i * baseDataSet[6])
        ])
    return data

def genRealData():
    ''' Populates a data array with a sample of real data from AAPL using fake dates
    '''
    data = []
    data.append( [dt.now() - td(18) + (td(1) * 0), 171.51, 174.77, 170.88, 174.24, 174.24, 41387400] )
    data.append( [dt.now() - td(18) + (td(1) * 1), 176.73, 181.29, 174.93, 180.94, 180.94, 46062500] )
    data.append( [dt.now() - td(18) + (td(1) * 2), 182.66, 182.8, 177.7, 179.55, 179.55, 41770000] )
    data.append( [dt.now() - td(18) + (td(1) * 3), 180.29, 180.33, 177.35, 177.44, 177.44, 39531500] )
    data.append( [dt.now() - td(18) + (td(1) * 4), 184.46, 184.94, 181.21, 184.82, 184.82, 40653600] )
    
    return data

def checkListAssert(testCase : unittest.TestCase, list1, list2):
    '''Checks the number based list for almost equality (for floating point comparisons)
    '''
    testCase.assertEqual(len(list1), len(list2))
    for i in range(len(list1)):
        testCase.assertAlmostEqual(list1[i], list2[i])

def checkListEqAssert(testCase : unittest.TestCase, list1, list2):
    '''Checks the list for full equality (should be used for all but floating point comparisons)
    '''
    testCase.assertEqual(len(list1), len(list2))
    for i in range(len(list1)):
        testCase.assertEqual(list1[i], list2[i])

def createTestDatabase(dataMan):
    '''Sets up a testing database to use for unit testing, including fake data
    table stock_list contains the names for each of the fake data sets and mirrors its actual counterpart in structure
    database name is testBase
    '''
    dataMan.checkDatabaseExistence("testBase", create=True)
    dataMan.switch_database("testBase")
    dataMan.checkTableExistence("stock_list", create=True, columnDeclarationList=stockListTableCreationColList)
    dataMan.checkTableExistence("pos_yahoo_data", create=True, columnDeclarationList= tickerDataTableCreationColList)
    dataMan.checkTableExistence("real_yahoo_data", create=True, columnDeclarationList= tickerDataTableCreationColList)
    dataMan.checkTableExistence("switchback_yahoo_data", create=True, columnDeclarationList= tickerDataTableCreationColList)

    dataMan.insert_into_table("stock_list", stockListTableColList, [["pos", True, False]])
    dataMan.insert_into_table("stock_list", stockListTableColList, [["real", True, False]])
    dataMan.insert_into_table("pos_yahoo_data", tickerDataTableColList, genPosData())
    dataMan.insert_into_table("real_yahoo_data", tickerDataTableColList, genRealData())

class VolumeDataProcessingTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''Does first time database creation for all test runs (as no data should be modified, just read)
        '''
        loginCredential = config_handling()
        dataMan = MYSQLDataManipulator(loginCredential[0], loginCredential[1], loginCredential[2])
        createTestDatabase(dataMan)
        dataMan.close(commit=True)

    @classmethod
    def tearDownClass(cls):
        '''Does tear down of database
        '''
        loginCredential = config_handling()
        dataMan = MYSQLDataManipulator(loginCredential[0], loginCredential[1], loginCredential[2], "testBase")
        dataMan.execute_sql("drop schema testBase;")
        dataMan.close()

    def setUp(self):
        '''Sets up instance variables
        '''
        loginCredential = config_handling()
        loginCredential[3] = "testBase"
        self.dataProc = VolumeDataProcessor(loginCredential)

    def tearDown(self):
        '''Closes data objects'''
        self.dataProc.close()
    
    def testCalculateSignedPercentageChanges(self):
        percentageChanges = self.dataProc.calculatePercentageChanges()
        self.assertEqual(len(percentageChanges.tickers), 2)
        posData = percentageChanges.tickers[0].data
        posData = [x[1] for x in posData]
        realData = percentageChanges.tickers[1].data
        realData = [x[1] for x in realData]
        checkListAssert(self, posData, expectedSignedPercentageChangeResultsPos)
        checkListAssert(self, realData, expectedSignedPercentageChangeResultsReal)
        

    def testCalculateUnsignedPercentageChanges(self):
        percentageChanges = self.dataProc.calculatePercentageChanges(signed=False)
        self.assertEqual(len(percentageChanges.tickers), 2)
        posData = percentageChanges.tickers[0].data
        posData = [x[1] for x in posData]
        realData = percentageChanges.tickers[1].data
        realData = [x[1] for x in realData]
        checkListAssert(self, posData, expectedUnsignedPercentageChangeResultsPos)
        checkListAssert(self, realData, expectedUnsignedPercentageChangeResultsReal)

    def testCalculateSignedLimitedNumericChanges(self):
        lnc = self.dataProc.calculateLimitedNumericChange()
        self.assertEqual(len(lnc.tickers), 2)
        posData = lnc.tickers[0].data
        posData = [x[1] for x in posData]
        realData = lnc.tickers[1].data
        realData = [x[1] for x in realData]
        checkListAssert(self, posData, expectedSignedLNCResultsPos)
        checkListAssert(self, realData, expectedSignedLNCResultsReal)
        

    def testCalculateUnsignedLimitedNumericChanges(self):
        lnc = self.dataProc.calculateLimitedNumericChange(signed=False)
        self.assertEqual(len(lnc.tickers), 2)
        posData = lnc.tickers[0].data
        posData = [x[1] for x in posData]
        realData = lnc.tickers[1].data
        realData = [x[1] for x in realData]
        checkListAssert(self, posData, expectedUnsignedLNCResultsPos)
        checkListAssert(self, realData, expectedUnsignedLNCResultsReal)

    def testCalculateSignedMovementDirections(self):
        movementDirections = self.dataProc.calculateMovementDirections()
        self.assertEqual(len(movementDirections.tickers), 2)
        posData = movementDirections.tickers[0].data
        posData = [x[1] for x in posData]
        realData = movementDirections.tickers[1].data
        realData = [x[1] for x in realData]
        checkListEqAssert(self, posData, expectedSignedMovementDirectionResultsPos)
        checkListEqAssert(self, realData, expectedSignedMovementDirectionResultsReal)

    def testCalculateUnsignedMovementDirections(self):
        movementDirections = self.dataProc.calculateMovementDirections(signed=False)
        self.assertEqual(len(movementDirections.tickers), 2)
        posData = movementDirections.tickers[0].data
        posData = [x[1] for x in posData]
        realData = movementDirections.tickers[1].data
        realData = [x[1] for x in realData]
        checkListEqAssert(self, posData, expectedUnsignedMovementDirectionResultsPos)
        checkListEqAssert(self, realData, expectedUnsignedMovementDirectionResultsReal)