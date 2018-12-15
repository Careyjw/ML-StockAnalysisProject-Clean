from SharedGeneralUtils.SharedGeneralUtilityFunctions import config_handling, getModelFiles
from SharedGeneralUtils.SharedGeneralUtilityFunctions import loadModel, parseModelString, genPredictionData, genClients

from SharedGeneralUtils.EMessageTemplates import devTickerPredEM

from EmailUtils.EMessageSender import EMessageSender

from argparse import ArgumentParser

if __name__ == "__main__":
    argParser = ArgumentParser(description="Loads currently trained models and uses them to make a prediction for the following day")

    argParser.add_argument('-password', dest = "p", type = str, help="Password for the email sending system", required=True)
    namespace = argParser.parse_args()

    emailSys = EMessageSender("smtp.gmail.com", 465, "mlstockpredictions@gmail.com", namespace.p)

    clients = genClients()

    loginCredentials = config_handling()
    modelFiles = getModelFiles()
    
    msg = devTickerPredEM.multiplyKey("{ticker}", len(modelFiles))

    for x in modelFiles:
        modelTypeName, ticker, fileExtension = parseModelString(path.split(x)[1])
        model = loadModel(fileExtension, x)
        predData = genPredictionData(modelTypeName, ticker, loginCredentials, 10)
        res = model.predict(predData)
        msg = msg.replaceKey("{ticker}", "Volume Movement Direction Result for {0}: {1}".format(ticker, res), 1)

    for cli in clients:
        sendMsg = msg.replaceKey("{customer}", cli.clientName)
        emailSys.sendMessage(sendMsg, cli)
    emailSys.close()