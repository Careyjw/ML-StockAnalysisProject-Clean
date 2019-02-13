from os.path import exists
from typing import List
from Email.EClient import EClient
from Email.EMessage import EMessage
from Email.EMessageSender import EMessageSender


class EDispatcher:

    def __init__(self, filename : str, emailSender : "EMessageSender"):
        '''Intializes object
        :param filename: Path to the file to load the EDispatcher object from
        :param emailSender: EMessageSender object to send messages with
        '''
        self.clients : List["EClient"] = []
        self.load(filename)
        self.messageSender = emailSender

    def sendMessage(self, eMessage : "EMessage"):
        '''Sends message to all applicable clients
        :param eMessage: Message to send to all applicable clients
        '''
        for cli in self.clients:
            if(cli.shouldSendMessage(eMessage)):
                self.messageSender.sendMessage(eMessage, client)

    def addClient(self, client : "EClient"):
        '''Adds client to the contained client list
        '''
        self.clients.add(client)

    def load(self, filename : str):
        '''Loads object from the given file

        '''
        if not (exists(filename)):
            return
        fileHandle = open(filename, "r")
        loadedClient = EClient.load(fileHandle)
        while not loadedClient = None:
            self.clients.append(loadedClient)
            loadedClient = EClient.load(fileHandle)
        fileHandle.close()
    
    def save(self, filename : str):
        '''Saves object to the given file
        '''    
        fileHandle = open(filename, "w")
        for cli in self.clients:
            cli.save(fileHandle)
        fileHandle.close()        