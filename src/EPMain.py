from argparse import ArgumentParser
from Common.Util.CommonFunctions import loginCredentialAssembling
from Evaluate.Evaluate import LoadModels, EvaluateModels
from getpass import getpass

def parseArgs():
    argParser = ArgumentParser(description="Evaluation and Prediction main file. Must be runa fter Model Training has generated at least one model")
    argParser.add_argument("-dp", dest="dp", default=getpass("Database Password:"), help="Password required to access the database")
    argParser.add_argument("-ep", dest="ep", default=getpass("Email System Password:"), help = "Password required for accessing email system")
    return argParser.parse_args()


if __name__ == "__main__":
    namespace = parseArgs()
    loginCredentials = loginCredentialAssembling(namespace.dp)
    models = LoadModels(loginCredentials)
    EvaluateModels(models)