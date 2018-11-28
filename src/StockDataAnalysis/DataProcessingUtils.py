'''
Created on Nov 27, 2018

@author: Colton Freitas
'''
from DatabaseUtils.MySQLUtils import MYSQLDataManipulator


class DataProcessor:
    
    def __init__(self, login_credentials):
        '''
        
        @param login_credentials: List of credentials in format specified below
        @format login_credentials: [host, user, password, database (can be None)]
        '''
        
        self.dataManager = MYSQLDataManipulator(login_credentials[0], login_credentials[1], login_credentials[2], login_credentials[3])
        
