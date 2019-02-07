from SharedGeneralUtils.SharedGeneralUtilityFunctions import config_handling, getModelFiles, parseEvalModelString, genEvalData
from SharedGeneralUtils.SharedGeneralUtilityFunctions import loadModel, parseModelString, genPredictionData, genClients
from SharedGeneralUtils.CommonValues import modelStoragePathBase, evaluationModelStoragePathBase, startDate

from SharedGeneralUtils.EMessageTemplates import devTickerPredEM

from EmailUtils.EMessageSender import EMessageSender

from os import path

from argparse import ArgumentParser

if __name__ == "__main__":
    argParser = ArgumentParser(description="Loads currently trained models and uses them to make a prediction for the following day")

    argParser.add_argument('-password', dest = "p", type = str, help="Password for the email sending system", required=True)
    argParser.add_argument('-evalMode', dest = "e", type = bool, help="Determines whether to evaluate models in the training directory instead of making predictions", default=False)
    
    argParser.add_argument('-max_training_tickers', dest="m", type=int, nargs=1, help="The maximum number of other (similar) stocks that will be used to make the model more accurate.", default=4)
    argParser.add_argument('-min_similarity', dest="s", type=float, nargs=1, help="The minimum amount of similarity required for a stock to be eligible as a part of the training set.", default = .6)
    argParser.add_argument('-num_days_per_example', dest = "de", type=int, nargs = 1, help="The number of days to use for one training example", default = 14)
    
    argParser.add_argument('-evalPeriodLen', dest="ep", type=int, nargs=1, help="The number of days to group into one evaluation period.", default = 30)

    namespace = argParser.parse_args()

    emailSys = EMessageSender("smtp.gmail.com", 465, "mlstockpredictions@gmail.com", namespace.p)

    clients = genClients()

    loginCredentials = config_handling()
    clusterFunctionArgs = [namespace.s, namespace.m, namespace.de, startDate]

    if not namespace.e:
        modelFiles = getModelFiles(modelStoragePathBase)
        msg = devTickerPredEM.multiplyKey("{ticker}", len(modelFiles))
        for currModelFile in modelFiles:
            modelTypeName, ticker, fileExtension = parseModelString(path.split(currModelFile)[1])
            model = loadModel(fileExtension, currModelFile)
            predData = genPredictionData(modelTypeName, ticker, loginCredentials, namespace.de, clusterFunctionArgs)
            res = model.predict(predData)
            msg = msg.replaceKey("{ticker}", "Volume Movement Direction Result for {0}: {1}".format(ticker, res), 1)

        for cli in clients:
            sendMsg = msg.replaceKey("{customer}", cli.clientName)
            emailSys.sendMessage(sendMsg, cli)
    else:
        modelFiles = getModelFiles(evaluationModelStoragePathBase)

        for currModelFile in modelFiles:
            modelTypeName, ticker, epochsTrained, fileExtension = parseEvalModelString(path.split(currModelFile)[1])
            model = loadModel(fileExtension, currModelFile)
            predData, evalData, dataStorage = genEvalData(modelTypeName, ticker, loginCredentials, namespace.de, clusterFunctionArgs)
            numCorrect = 0
            for i in range(len(predData)):
                dataStorage.addPredictionData(predData[i])
                res = model.predict(dataStorage)
                if (res == evalData[i][0]):
                    numCorrect += 1
                if i % namespace.ep == 0 and not i == 0:
                    print("Prediction accuracy of {0} at day {2}: {1}".format(
                        "{0}_{1}:{2}".format(modelTypeName, ticker, epochsTrained), (numCorrect / (i+1)) * 100, i+1
                    ))
            print("Prediction accuracy of {0} for full period: {1} ".format(
                "{0}_{1}:{2}".format(modelTypeName, ticker, epochsTrained), (numCorrect / len(predData)) * 100
                ))


    emailSys.close()