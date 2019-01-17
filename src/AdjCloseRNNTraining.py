'''
:author: Colton Freitas
:as-of: Dec 10, 2018
Trains models from volume data
'''

from StockDataAnalysis.ClusteringFunctionStorage import movingAverageClustering

from StockDataPrediction.ModelTrainingPipeline import ModelTrainingPipeline
from StockDataPrediction.TrainingFunctionStorage.TrainingFunctionStorage import trainCloseRNNMovementDirections

from SharedGeneralUtils.SharedGeneralUtilityFunctions import config_handling, get_stock_list
from SharedGeneralUtils.CommonValues import startDate

from argparse import ArgumentParser

from os import cpu_count
from datetime import datetime, timedelta



if __name__ == "__main__":

    argParser = ArgumentParser(description="Module for training Recurrent Neural Networks on Volumetric data to predict stock price movements")
    argParser.add_argument('-max_processes', dest="p", type=int, help="The maximum number of processes this script is allowed to create.", default=cpu_count())
    argParser.add_argument('-clustering_processes', dest = "cp", type = int, help = "The number of processes to dedicate to training models", default = -1)
    argParser.add_argument('-training_processes', dest = "tp", type = int, help = "The number of processes to dedicate to clustering similar stocks", default = -1)
    
    argParser.add_argument('-max_training_tickers', dest="m", type=int, help="The maximum number of other (similar) stocks that will be used to make the model more accurate.", default=4)
    argParser.add_argument('-min_similarity', dest="e", type=float, help="The minimum amount of similarity required for a stock to be eligible as a part of the training set.", default = .6)
    argParser.add_argument('-num_days_per_example', dest = "de", type=int, help="The number of days to use for one training example", default = 14)

    argParser.add_argument('-rnn_hidden_state_size', dest = "h", type = int, help = "The size of the hidden state in the RNN model", default = 200)
    argParser.add_argument('-rnn_backpropagation_truncation_amount', dest = "t", type=int, help = "The number of layers back the model should use in the backprogation algorithm to calculate the gradient for the current layer.", default = 5)
    argParser.add_argument('-rnn_learning_rate', dest = 'l', type = float, help = "The initial learning rate for the RNN model, if one is not selected, this does nothing.", default = 0.1)
    argParser.add_argument('-rnn_loss_eval', dest = 'le', type = bool, help = "How many epochs should be completed before evaluating the loss in the model", default = 5)

    argParser.add_argument('-rnn_num_epochs', dest = "ne", type = int, help = "The number of epochs the model should be trained for, this value is meaningless if the model is being trained until convergence.", default = 1500)


    namespace = argParser.parse_args()

    maxProcesses = namespace.p
    clusteringProcesses = 1 if namespace.cp <= 0 else namespace.cp
    trainingProcesses = maxProcesses-1 if namespace.tp <= 0 else namespace.tp


    pipeline = ModelTrainingPipeline(namespace.p, config_handling(), namespace.cp, namespace.tp)

    clusterFunctionArgs = [namespace.e, namespace.m, namespace.de, startDate]
    trainingFunctionArgs = [startDate, (namespace.h, namespace.t, namespace.l, namespace.le), namespace.ne, namespace.de]


    pipeline.usePipeline(get_stock_list(), trainCloseRNNMovementDirections, trainingFunctionArgs, movingAverageClustering, clusterFunctionArgs)