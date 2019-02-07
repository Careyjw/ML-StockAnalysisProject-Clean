from datetime import datetime, timedelta, date

startDate = date.fromtimestamp( (datetime.now() - timedelta(365)).timestamp() )
evalStartDate = startDate - timedelta(365)

stockTickerFileLocation = "../configuration_data/stock_list.txt"
configurationFileLocation = "../configuration_data/config.ini"

modelStoragePathBase = "../model_storage/{0}"
evaluationModelStoragePathBase = modelStoragePathBase.format("training/{0}")

LimitedNumericChangeSourceID = "LimitedNumericChangeCalculator"
MovementDirectionSourceID = "MovementDirectionCalculator"
PercentageChangesSourceID = "PercentageChangesCalculator"

AdjestedMovementDirectionSegmentedID = "ACMDS"
VolumeMovementDirectionsSegmentedID = "VMDS"
VolumeLNCSegmentedID = "VLNCS"