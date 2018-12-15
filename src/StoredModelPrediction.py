from SharedGeneralUtils.SharedGeneralUtilityFunctions import config_handling, getModelFiles
from SharedGeneralUtils.SharedGeneralUtilityFunctions import loadModel, parseModelString, genPredictionData, genClients

from SharedGeneralUtils.EMessageTemplates import devTickerPredEM

from EmailUtils.EMessageSender import EMessageSender

from os import path

if __name__ == "__main__":
    emailSys = EMessageSender("smtp.gmail.com", 465, "mlstockpredictions@gmail.com", "PrayersAndFaith")

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