from AI.SingleDataCategoryRNN import SingleDataCategoryRNN
#LEAVE THE ABOVE IMPORT(S)
#THIS IS WHAT CALLS THE ANNOTATION THAT REGISTERS THE CLASS
#REMOVING IT MAY BREAK THE PROGRAM.

from argparse import ArgumentParser
from Common.Util.CommonFunctions import loginCredentialAssembling
from Evaluate.Evaluate import Evaluate
from Prediction.Prediction import Predict
from Email.EMessageSender import EMessageSender
from Email.EClientGeneration import genClients
from getpass import getpass

def parseArgs():
    argParser = ArgumentParser(description="Evaluation and Prediction main file. Must be runa fter Model Training has generated at least one model")
    argParser.add_argument("-dp", dest="dp", default="", help="Password required to access the database")
    argParser.add_argument("-ep", dest="ep", default="", help = "Password required for accessing email system")
    argParser.add_argument("-e", dest="e", default = False, help = "Flag for whether to evaluate models or predict models. Evaluation happens when flag is True")
    argParser.add_argument("-o", dest='o', default = False, help = "Boolean flag for whether to output evaluation to stdout. If this is true, then the email system password is ignored")

    namespace = argParser.parse_args()
    if(namespace.dp == ""):
        namespace.dp = getpass("Database Password:")
    if (namespace.ep == ""):
        namespace.ep = getpass("Email System Password:")
    
    if (namespace.e == "False"):
        namespace.e = False
    if (namespace.o == "False"):
        namespace.o == False

    return namespace


if __name__ == "__main__":
    namespace = parseArgs()
    loginCredentials = loginCredentialAssembling(namespace.dp)
    
    emailSys = None

    if not namespace.o:
        emailSys = EMessageSender("smtp.gmail.com", 465, "mlstockpredictions@gmail.com", namespace.ep)
    

    clients = genClients()

    if (namespace.e):
        Evaluate(loginCredentials, emailSys, clients, namespace.o)
    else:
        Predict(loginCredentials, emailSys, clients, namespace.o)
    