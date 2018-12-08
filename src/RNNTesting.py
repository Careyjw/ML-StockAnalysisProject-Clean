from StockDataPrediction.MachineLearningModels.SingleDataCateogryRNN import RNNNormal
from StockDataPrediction.MachineLearningModels.TrainingDataStorages import RNNTrainingDataStorage


def normData(x):
    return int(x)

if __name__ == "__main__":
    dataStorage = RNNTrainingDataStorage(normData, normData)
    rnn = RNNNormal(200, 11, 2)
    dataStorage.addTrainingExample( [[2,3], [3,4], [5,5]], [5, 7, 10] )
    rnn.trainEpoch_BatchGradientDescent(dataStorage, batchGradientSize=1, numEpochs=200)
