from typing import List

class EMessage:

    @classmethod
    def loadFromFile(cls, filepath : str):
        '''Loads EMessage object from file
        :param filepath: path to the file to read in
        '''
        fileHandle = open(filepath, "r")
        identificationLine = fileHandle.readline()
        subject = fileHandle.readline()
        defaultMessageStatus = bool(fileHandle.readline())
        ident, subIdent = identificationLine.strip().split(":")
        subIdent = subIdent.split(",")
        body = "".join([x for x in fileHandle])
        fileHandle.close()
        return EMessage(body, ident, subject, subIdent, defaultMessageStatus)


    def __init__(self, body : str, identifier : str, subject : str, subIdentifiers : List['EMessage'], defaultMessageStatus : bool = False):
        '''Initializes object
        :param body: body of the email message
        :param identifier: identifier of message type for message filtering
        :param subIdentifiers: List of sub identifiers for further message filtering
        '''
        self.body = body
        self.identifier = identifier
        self.subject = subject
        self.subIdentifiers = subIdentifiers
        self.defaultMessageStatus = defaultMessageStatus

    def __str__(self):
        return self.body

    def __repr__(self):
        return str(self)

    def multiplyKey(self, text : str, amnt : int) -> 'EMessage':
        '''Searches the body for the first instance of text and copies it amnt times
        :param text: text to search the body for
        :param amnt: amount of times to copy the listed text
        :return: EMessage instance with the modified body
        '''
        body = self.body.replace(text, "\n".join([text] * amnt))
        return EMessage(body, self.identifier, self.subIdentifiers)

    def replaceKey(self, text : str, eMessage, amnt : int = 1) -> 'EMessage':
        '''Searches the body for text matching text, and replaces it with eMessage
        :param text: text to search the body for
        :param eMessage: Message to replace the text with
        :type eMessage: str or EMessage
        :param amnt: amount of matching text locations to replace
        :return: EMessage instance with the modified body
        '''
        body = ""
        if (type(eMessage) == type("")):
            body = self.body.replace(text, eMessage, amnt)
        elif (type(eMessage) == type(self)):
            body = self.body.replace(text, eMessage.body, amnt)
        
        return EMessage(body, self.identifier, self.subIdentifiers)

    def addSubIdentifier(self, identifier : str):
        '''Adds the identifier to the current list of subIdentifiers
        :param identifier: identifier to add
        '''
        if not identifier in self.subIdentifiers:
            self.subIdentifiers.append(identifer)
    
    def saveToFile(self, filepath : str):
        '''Saves current EMessage object to file
        :param filepath: path to the file to write to
        '''

        fileHandle = open(filepath, "w")
        fileHandle.write(
            "{0}:{1}\n".format(self.identifier, ",".join(self.subIdentifiers))
        )
        fileHandle.write(self.subject + "\n")
        fileHandle.write(self.defaultMessageStatus + "\n")
        fileHandle.write(self.body)
        fileHandle.close()