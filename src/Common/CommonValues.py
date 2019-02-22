from datetime import datetime, timedelta, date
from configparser import ConfigParser

startDate = date.fromtimestamp( (datetime.now() - timedelta(365)).timestamp() )
evalStartDate = startDate - timedelta(365)

stockTickerFileLocation = "../configuration_data/stock_list.txt"
configurationFileLocation = "../configuration_data/config.ini"
modelConfigurationFileLocation = "../configuration_data/model_config.ini"

modelStoragePathBase = "../model_storage/{0}"
evaluationModelStoragePathBase = modelStoragePathBase.format("evaluation_training/{0}")

LimitedNumericChangeSourceID = "LimitedNumericChangeCalculator"
MovementDirectionSourceID = "MovementDirectionCalculator"
PercentageChangesSourceID = "PercentageChangesCalculator"

AdjestedMovementDirectionSegmentedID = "ACMDSC"
VolumeMovementDirectionsSegmentedID = "VMDSC"
VolumeLNCSegmentedID = "VLNCSC"

modelConfiguration = ConfigParser()