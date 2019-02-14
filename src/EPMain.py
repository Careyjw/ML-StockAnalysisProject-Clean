from argparse import ArgumentParser

def parseArgs():
    argParser = ArgumentParser(description="Evaluation and Prediction main file. Must be runa fter Model Training has generated at least one model")
    argParser.add_argument("-dp", dest="dp", required=True, help="Password required to access the database")
    argParser.add_argument("-ep", dest="ep", required=True, help = "Password required for accessing email system")
    return argParser.parse_args()


if __name__ == "__main__":
    pass