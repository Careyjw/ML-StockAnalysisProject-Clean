from Email.ClientFilterTemplates import devClientFilter
from Email.EClient import EClient

def genClients():
    '''Generates a quick list of clients to send data to.
    :status: temporary, will need to be replaced
    '''
    jimClient = EClient("Jim Carey", "careyjw@plu.edu", devClientFilter)
    coltonClient = EClient("Colton Freitas", "freitacr@plu.edu", devClientFilter)
    return [jimClient, coltonClient]