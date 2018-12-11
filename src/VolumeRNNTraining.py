'''
:author: Colton Freitas
:as-of: Dec 10, 2018
Trains models from volume data
'''

from StockDataAnalysis.ClusteringFunctionStorage import movingAverageClustering, setClusterFunctionArgs, setStartDate, clusterFunctionArguments
from StockDataPrediction.ModelTrainingPipeline import ModelTrainingPipeline
from StockDataPrediction.TrainingFunctionStorage.TrainingFunctionStorage import trainVolumeRNNMovementDirections
from SharedGeneralUtils.SharedGeneralUtils import config_handling
from os import cpu_count
from datetime import datetime, timedelta



if __name__ == "__main__":
    pipeline = ModelTrainingPipeline(cpu_count(), config_handling(), 1, cpu_count() - 1)
    startDate = datetime.now() - timedelta(365)
    clusterFunctionArgs = [.60, 5, 15, startDate]
    trainingFunctionArgs = [startDate, (200, 5, .1, 5), 200, 10]


    pipeline.usePipeline(["AAPL", "T"], trainVolumeRNNMovementDirections, trainingFunctionArgs, movingAverageClustering, clusterFunctionArgs)