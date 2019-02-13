from typing import List, IO
from Email.EMessage import EMessage

class EClient:

    def __init__(self, clientName : str, clientAddress : str, clientFilter = None):
        self.clientName = clientName
        self.clientAddress = clientAddress
        self.clientFilter = clientFilter
        if self.clientFilter == None:
            self.clientFilter = EClientFilter()

    def replaceFilter(self, clientFilter : "EClientFilter"):
        '''Replaces the current filter for the client using the supplied filter
        '''
        self.clientFilter = clientFilter

    def updateFilter(self, clientFilter : "EClientFilter"):
        '''Updates the current filter for the client using the supplied filter
        '''
        self.clientFilter = clientFilter + self.clientFilter

    def shouldSendMessage(self, eMessage : "EMessage")->bool:
        '''Determines whether the message should be sent to the current client
        '''
        return self.clientFilter.filterMessage(eMessage)

    @classmethod
    def load(cls, fileHandle):
        '''Loads EClient object from the open fileHandle'''
        clientName = fileHandle.readline().strip()
        clientAddress = fileHandle.readline().strip()
        cliFilter = EClientFilter()
        cliFilter.load(fileHandle)
        return EClient(clientName, clientAddress, cliFilter)

    def save(self, fileHandle : IO):
        '''Saves the EClient to the open fileHandle'''
        fileHandle.write(self.clientName + "\n")
        fileHandle.write(self.clientAddress + "\n")
        self.clientFilter.store(fileHandle)

class EClientFilter:

    class EClientFilterIdentifier:
        
        def __init__(self, allowedIdentifier : str, requiredSubIdentifiers: List[str]):
            '''Constructs EClientFilterIdentifier object
            :param allowedIdentifier: messageIdentifier to match with
            :param requiredSubIdentifiers: list of all sub identifiers that MUST be in the message's sub identifiers to be considered a match
            '''
            self.allowedIdentifier = allowedIdentifier
            self.requiredSubIdentifiers = requiredSubIdentifiers

        def isMatch(self, eMessage : EMessage) -> bool:
            '''Returns if eMessage matches the identification parameters of this filter
            '''
            if self.allowedIdentifier == eMessage.identifier or self.allowedIdentifier == "ANY":
                for x in self.requiredSubIdentifiers:
                    if not x in eMessage.subIdentifiers:
                        return False
                return True
            return False

        @classmethod
        def parseSelf(cls, line):
            '''Parse line and create an EClientFilterIdentifier object if the line contains it
            '''
            if line.strip() == "":
                return None
            identifier, subIdentifiers = line.strip().split(":")
            subIdentifiers = [x for x in subIdentifiers.split(",")]
            subIdentifiers = [x for x in subIdentifiers if not x == ''] #Remove empty sub identifiers
            return EClientFilter.EClientFilterIdentifier(identifier, subIdentifiers)

        def __str__(self):
            return "{0}:{1}".format(self.allowedIdentifier, ",".join(self.requiredSubIdentifiers))

        def __repr__(self):
            return str(self)

        def __eq__(self, other):
            '''Defines equality between EClientFilterIdentifier objects
            '''
            if not type(other) == type(self):
                return False
            else:
                if (self.allowedIdentifier == other.allowedIdentifier):
                    for x in self.requiredSubIdentifiers:
                        if not x in other.requiredSubIdentifiers:
                            return False
                    for x in other.requiredSubIdentifiers:
                        if not x in self.requiredSubIdentifiers:
                            return False
                    return True
                return False


    def __init__(self):
        self.whitelistIdentifiers : List['EClientFilterIdentifier'] = []
        self.blacklistIdentifiers : List['EClientFilterIdentifier'] = []

    def addWhitelistEntry(self, messageIdentifier : str, messageSubIdentifiers : List[str] = None):
        '''Adds an EClientFilterIdentifier object and adds it to the whitelist
        '''
        if not messageSubIdentifiers == None:
            self.whitelistIdentifiers.append(EClientFilter.EClientFilterIdentifier(messageIdentifier, messageSubIdentifiers))
        else:
            self.whitelistIdentifiers.append(EClientFilter.EClientFilterIdentifier(messageIdentifier))

    def addBlacklistEntry(self, messageIdentifier : str, messageSubIdentifiers : List[str] = None):
        '''Adds an EClientFilterIdentifier object and adds it to the blacklist
        '''
        if not messageSubIdentifiers == None:
            self.blacklistIdentifiers.append(EClientFilter.EClientFilterIdentifier(messageIdentifier, messageSubIdentifiers))
        else:
            self.blacklistIdentifiers.append(EClientFilter.EClientFilterIdentifier(messageIdentifier))
    
    def store(self, fileHandle):
        '''Stores EClientFilter object using open filehandle
        '''
        fileHandle.write("whitelist:\n")
        
        fileHandle.write(
            "\n".join([str(x) for x in self.whitelistIdentifiers])
        )
        fileHandle.write("\n")
        fileHandle.write("blacklist:\n")
        fileHandle.write(
            "\n".join([str(x) for x in self.blacklistIdentifiers])
        )
        
        fileHandle.write("\n")

    def load(self, fileHandle):
        '''Loads EClientFilter object in from open filehandle
        '''
        line = fileHandle.readline() #eat whitelist declaration
        if line.strip() == '':
            return None
        line = fileHandle.readline()
        while not line.strip() == "":
            whitelistID = EClientFilter.EClientFilterIdentifier.parseSelf(line)
            if not whitelistID == None:
                self.whitelistIdentifiers.append(whitelistID)
            line = fileHandle.readline()
        line = fileHandle.readline() #eat blacklist declaration
        line = fileHandle.readline()
        while not line.strip() == "":
            blacklistID = EClientFilter.EClientFilterIdentifier.parseSelf(line)
            if not blacklistID == None:
                self.blacklistIdentifiers.append(blacklistID)
            line = fileHandle.readline()
        
    def __combine(self, other : 'EClientFilter') -> 'EClientFilter':
        '''Combines two instances of EClientFilter together into a combined filter
        :param other: the filter to combine with
        '''

        retFilter = EClientFilter()
        
        for blackListIdent in other.blacklistIdentifiers:
            for whitelistIdent in self.whitelistIdentifiers:
                if (blackListIdent == whitelistIdent):
                    raise FilterCombinationError("Whitelist and Blacklist contain identical identifiers")
                retFilter.addBlacklistEntry(blackListIdent.allowedIdentifier, blackListIdent.requiredSubIdentifiers)
        for whitelistIdent in other.whitelistIdentifiers:
            for blackListIdent in self.blacklistIdentifiers:
                if (blackListIdent == whitelistIdent):
                    raise FilterCombinationError("Whitelist and Blacklist contain identical identifiers")
                retFilter.addWhitelistEntry(whitelistIdent.allowedIdentifier, whitelistIdent.requiredSubIdentifiers)
        for whitelistIdent in self.whitelistIdentifiers:
            retFilter.addWhitelistEntry(whitelistIdent.allowedIdentifier, whitelistIdent.requiredSubIdentifiers)
        for blackListIdent in self.blacklistIdentifiers:
            retFilter.addBlacklistEntry(blackListIdent.allowedIdentifier, blackListIdent.requiredSubIdentifiers)

        

        return retFilter

    def __add__(self, other : 'EClientFilter'):
        '''Combines two EClientFilter objects together
        '''
        if not type(other) == type(self):
            return None
        else:
            return self.__combine(other)

    def filterMessage(self, eMessage : EMessage) -> bool:
        '''Determines if the eMessage should be passed through the filter
        :return: True if the eMessage passed filtering, false otherwise
        
        '''

        for ident in self.whitelistIdentifiers:
            if (ident.isMatch(eMessage)):
                return True
        for ident in self.blacklistIdentifiers:
            if (ident.isMatch(eMessage)):
                return False
        return eMessage.defaultMessageStatus

    #def __str__(self):
        
class FilterCombinationError(Exception):
    '''Raised when combining filters goes wrong'''
    pass