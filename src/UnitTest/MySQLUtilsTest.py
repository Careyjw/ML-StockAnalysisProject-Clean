import unittest
from DatabaseUtils import MySQLUtils as utils
import Common.Util.CommonFunctions as genUtils
from datetime import datetime as dt
from datetime import date



class MySQLUtilsTest (unittest.TestCase):        

    def setUp(self):
        self.login_credentials = genUtils.config_handling()
        self.data_man = utils.MYSQLDataManipulator(self.login_credentials[0],self.login_credentials[1], self.login_credentials[2], self.login_credentials[3])
        self.columnDeclarationList = [["id", "int primary key auto_increment"], ["name", "text"]]
        self.columnNameList = [x[0] for x in self.columnDeclarationList if not x[0] == "id"]
        self.columnDeclarationListNonString = [["id", "int primary key auto_increment"], ["storage", "Date"]]
        self.columnNameListNonString = [x[0] for x in self.columnDeclarationListNonString if not x[0] == "id"]
    
    def test_databaseCreate(self):
        testingBaseExists = self.data_man.checkDatabaseExistence("newBase")
        if (testingBaseExists):
            self.data_man.execute_sql("drop schema newBase;")
        self.assertFalse(self.data_man.checkDatabaseExistence("newBase"))
        self.assertTrue(self.data_man.create_database("newBase"))
        self.assertTrue(self.data_man.checkDatabaseExistence("newBase"))
        self.assertFalse(self.data_man.create_database("newBase"))
        self.data_man.execute_sql("drop schema newBase;")
        
    
    def test_databaseExistenceChecking(self):
        testingBaseExists = self.data_man.checkDatabaseExistence("newBase")
        if (testingBaseExists):
            self.data_man.execute_sql("drop schema newBase;")
        self.assertFalse(self.data_man.checkDatabaseExistence("newBase"))
        self.data_man.execute_sql("create schema newBase;")
        self.assertTrue(self.data_man.checkDatabaseExistence("newBase"))
        self.data_man.execute_sql("drop schema newBase;")
        self.assertFalse(self.data_man.checkDatabaseExistence("newBase"))
        pass

    def test_tableCreate(self):
        
        self.data_man.checkDatabaseExistence("newBase", create=True)
        self.data_man.switch_database("newBase")
        self.assertFalse(self.data_man.checkTableExistence("test_table"))
        self.data_man.create_table("test_table", self.columnDeclarationList)
        self.assertTrue(self.data_man.checkTableExistence("test_table"))
        self.data_man.execute_sql("drop table test_table;")
        self.data_man.execute_sql("drop schema newBase;")

    def test_tableExistence(self):
        self.columnDeclarationList = [" ".join(x) for x in self.columnDeclarationList]
        sql = "create table {0} ({1});".format("test_table", ",".join(self.columnDeclarationList))
        
        self.data_man.checkDatabaseExistence("newBase", create=True)
        self.data_man.switch_database("newBase")
        self.assertFalse(self.data_man.checkTableExistence("test_table"))
        self.data_man.execute_sql(sql)
        self.assertTrue(self.data_man.checkTableExistence("test_table"))
        self.data_man.execute_sql("drop table test_table;")
        self.data_man.execute_sql("drop schema newBase;")

    def testInsertIntoTableAndSelectFromTable(self):
        self.data_man.checkDatabaseExistence("newBase", create=True)
        self.data_man.switch_database("newBase")
        self.data_man.create_table("test_table", self.columnDeclarationList)
        self.data_man.insert_into_table("test_table", self.columnNameList, [["Hello"]])
        res = self.data_man.select_from_table("test_table", self.columnNameList)
        self.assertEqual(res[0][0], "Hello")

        #Test for non-string inputs
        self.data_man.create_table("test_table2", self.columnDeclarationListNonString)
        self.data_man.insert_into_table("test_table2", self.columnNameListNonString, [[dt.now()]])
        res = self.data_man.select_from_table("test_table2", self.columnNameListNonString)
        self.assertEqual(res[0][0], date.fromtimestamp(dt.now().timestamp()))

        self.data_man.execute_sql("drop table test_table;")
        self.data_man.execute_sql("drop schema newBase;")

    def tearDown(self):
        self.data_man.close(commit=False)
